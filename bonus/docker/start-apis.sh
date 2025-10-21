#!/bin/bash

echo "Iniciando todas as APIs..."

# Iniciar API Ex1 em background
cd /app/api/exercicio1
python app.py &
PID1=$!

# Iniciar API Ex2 em background
cd /app/api/exercicio2
python app.py &
PID2=$!

# Iniciar API Ex4 em background
cd /app/api/exercicio4
python app.py &
PID4=$!

# Iniciar API Ex6 em background
cd /app/api/exercicio6
python app.py &
PID6=$!

echo "APIs iniciadas:"
echo "- Ex1 (PID: $PID1) na porta 5001"
echo "- Ex2 (PID: $PID2) na porta 5002"
echo "- Ex4 (PID: $PID4) na porta 5004"
echo "- Ex6 (PID: $PID6) na porta 5006"

# Aguardar todos os processos
wait $PID1 $PID2 $PID4 $PID6
