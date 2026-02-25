import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";

interface User {
    id: number;
    email: string;
    full_name?: string | null;
}

function Home() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/login");
            return;
        }

        const fetchMe = async () => {
            try {
                const response = await api.get("/auth/me");
                setUser(response.data);
            } catch {
                localStorage.removeItem("token");
                navigate("/login");
            } finally {
                setLoading(false);
            }
        };
        fetchMe();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    if (loading) {
        return <p>Carregando...</p>;
    }

    if (!user) {
        return null;
    }

    return (
      <div style={{ maxWidth: 800, margin: "40px auto" }}>
      <h1>Mensageiro</h1>
      {user && (
        <p>
          Logado como <strong>{user.full_name || user.email}</strong>
        </p>
      )}
      <button onClick={handleLogout}>Sair</button>

      <hr />
      <p>Aqui depois vamos colocar a UI de templates e mensagens.</p>
    </div>
    );
}

export default Home;