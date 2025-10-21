// Configuração de URLs das APIs
const CONFIG = {
    // Para desenvolvimento local
    local: {
        ex1: 'http://localhost:5001/api/ex1',
        ex2: 'http://localhost:5002/api/ex2',
        ex4: 'http://localhost:5004/api/ex4',
        ex6: 'http://localhost:5006/api/ex6',
        ex3: 'http://localhost:8501',
        ex5: 'http://localhost:8000'
    },

    // Para produção AWS (substitua pelos valores reais após deploy)
    production: {
        ex1: 'https://api.seudominio.com/api/ex1',
        ex2: 'https://api.seudominio.com/api/ex2',
        ex4: 'https://api.seudominio.com/api/ex4',
        ex6: 'https://api.seudominio.com/api/ex6',
        ex3: 'https://app.seudominio.com/ex3',
        ex5: 'https://app.seudominio.com/ex5'
    }
};

// Detectar ambiente automaticamente
const ENV = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'local'
    : 'production';

// Exportar URLs ativas
const API_URLS = CONFIG[ENV];
