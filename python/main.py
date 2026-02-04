from flask import Flask, render_template_string
import socket

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hallo, Welt!</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: radial-gradient(circle at top, #1f1c2c, #928dab);
            color: white;
            overflow: hidden;
        }
        .card {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 18px;
            padding: 32px 36px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        }
        h1 {
            margin: 0 0 12px 0;
            font-size: 2.2rem;
        }
        p {
            margin: 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .emoji {
            font-size: 3rem;
            display: inline-block;
            margin-bottom: 16px;
            animation: bounce 1.6s ease-in-out infinite;
            filter: drop-shadow(0 6px 8px rgba(0, 0, 0, 0.35));
        }
        .sparkles {
            position: absolute;
            inset: 0;
            pointer-events: none;
            background-image:
                radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.25) 0 2px, transparent 2px),
                radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.2) 0 2px, transparent 2px),
                radial-gradient(circle at 40% 70%, rgba(255, 255, 255, 0.18) 0 2px, transparent 2px),
                radial-gradient(circle at 70% 80%, rgba(255, 255, 255, 0.15) 0 2px, transparent 2px);
            animation: drift 8s ease-in-out infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-12px) rotate(-2deg); }
        }
        @keyframes drift {
            0%, 100% { transform: translateY(0); opacity: 0.9; }
            50% { transform: translateY(-14px); opacity: 0.7; }
        }
    </style>
</head>
<body>
    <div class="sparkles"></div>
    <div class="card">
        <div class="emoji">🎉</div>
        <h1>Willkommen auf dem Mini‑Webserver!</h1>
        <p>Hab einen wunderbaren Tag — der Server freut sich, dich zu sehen.</p>
    </div>
</body>
</html>
"""
@app.route('/')
def index():
    """Hauptseite mit Begrüßung"""
    return render_template_string(HTML_TEMPLATE)


def get_local_ip():
    """Ermittelt die lokale IP-Adresse"""
    try:
        hostname = socket.gethostname()
        candidates = []

        try:
            _, _, ips = socket.gethostbyname_ex(hostname)
            candidates.extend(ips)
        except Exception:
            pass

        # Fallback: lokale Interface-IP über nicht-routbare Zieladresse bestimmen
        if not candidates:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("10.255.255.255", 1))
                candidates.append(s.getsockname()[0])
            finally:
                s.close()

        # Erste brauchbare IPv4 auswählen (nicht Loopback, nicht Link-Local)
        for ip in candidates:
            if ip and not ip.startswith("127.") and not ip.startswith("169.254."):
                return ip
    except:
        return "127.0.0.1"


if __name__ == '__main__':
    local_ip = get_local_ip()
    print("Starte Webserver...")
    print("=" * 50)
    print(f"🌐 Öffne im Browser:")
    print(f"   http://{local_ip}:80")
    print("=" * 50)
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
