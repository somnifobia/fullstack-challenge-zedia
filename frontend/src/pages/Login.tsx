import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            const response = await api.post("/auth/login", {
                email,
                password,
            });
            const { access_token } = response.data;
            console.log("token recebido:", access_token);
            localStorage.setItem("token", access_token);
            navigate("/");
        }   catch (err: any) {
            setError(
                err.response?.data?.detail ?? "Erro ao fazer login. Verifique os dados."
            );
        }   finally {
            setLoading(false);
        }
    };

    return (
      <div style={{ maxWidth: 400, margin: "80px auto" }}>
      <h1>Mensageiro - Login</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 16 }}>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: "100%" }}
          />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label>Senha</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: "100%" }}
          />
        </div>
        {error && (
          <p style={{ color: "red", marginBottom: 16 }}>
            {error}
          </p>
        )}
        <button type="submit" disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
}

export default Login;
    