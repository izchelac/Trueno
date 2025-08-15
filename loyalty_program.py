import json
import uuid
from pathlib import Path

DATA_FILE = Path(__file__).with_name("loyalty_data.json")
POINTS_PER_DRINK = 1
REDEEM_COST = 10


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"clients": {}}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def register_client(data, name, phone=None, email=None):
    cid = uuid.uuid4().hex[:8]
    data["clients"][cid] = {
        "name": name,
        "phone": phone,
        "email": email,
        "points": 0,
        "drinks": []
    }
    return cid


def add_points(data, client_id, points):
    data["clients"][client_id]["points"] += points


def record_drink(data, client_id, drink, free=False):
    data["clients"][client_id]["drinks"].append({"name": drink, "free": free})


def place_order(data, client_id, drink):
    record_drink(data, client_id, drink)
    add_points(data, client_id, POINTS_PER_DRINK)


def redeem_drink(data, client_id, drink):
    if data["clients"][client_id]["points"] < REDEEM_COST:
        raise ValueError("Not enough points")
    add_points(data, client_id, -REDEEM_COST)
    record_drink(data, client_id, drink, free=True)


def get_client(data, client_id):
    return data["clients"][client_id]


def show_client(data, client_id):
    client = get_client(data, client_id)
    lines = [
        f"Client: {client['name']}",
        f"Phone: {client.get('phone')}",
        f"Email: {client.get('email')}",
        f"Points: {client['points']}",
        "Drinks:" + ("" if client["drinks"] else " none"),
    ]
    for d in client["drinks"]:
        tag = "(free)" if d["free"] else ""
        lines.append(f"  - {d['name']} {tag}")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cafeteria loyalty program")
    sub = parser.add_subparsers(dest="cmd")

    reg = sub.add_parser("register")
    reg.add_argument("name")
    reg.add_argument("--phone")
    reg.add_argument("--email")

    add = sub.add_parser("add_points")
    add.add_argument("client_id")
    add.add_argument("points", type=int)

    order = sub.add_parser("order")
    order.add_argument("client_id")
    order.add_argument("drink")

    red = sub.add_parser("redeem")
    red.add_argument("client_id")
    red.add_argument("drink")

    show = sub.add_parser("show")
    show.add_argument("client_id")

    args = parser.parse_args()
    data = load_data()

    if args.cmd == "register":
        cid = register_client(data, args.name, args.phone, args.email)
        save_data(data)
        print("Client registered:", cid)
    elif args.cmd == "add_points":
        add_points(data, args.client_id, args.points)
        save_data(data)
    elif args.cmd == "order":
        place_order(data, args.client_id, args.drink)
        save_data(data)
    elif args.cmd == "redeem":
        try:
            redeem_drink(data, args.client_id, args.drink)
            save_data(data)
        except ValueError as e:
            print(e)
    elif args.cmd == "show":
        print(show_client(data, args.client_id))
    else:
        parser.print_help()
