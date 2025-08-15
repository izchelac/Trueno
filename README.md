# Trueno

Programa de lealtad para una cafetería.

## Uso

```bash
python loyalty_program.py register "Ana" --phone 555 --email ana@example.com
python loyalty_program.py order <client_id> "Latte"
python loyalty_program.py redeem <client_id> "Espresso"
python loyalty_program.py show <client_id>
```

Los clientes acumulan puntos por bebida comprada y pueden canjearlos por bebidas gratis.
