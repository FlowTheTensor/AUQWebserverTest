from flask import Flask, render_template_string
import socket

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webserver auf dem Arduino Uno Q</title>
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
            animation: day-night 24s ease-in-out infinite;
        }
        .card {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 18px;
            padding: 32px 36px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .card:hover {
            transform: rotate(-1deg) scale(1.02);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
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
        .letter {
            display: inline-block;
            transition: transform 0.2s ease;
        }
        .letter:hover {
            transform: rotate(12deg) scale(1.1);
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
        .stars {
            position: absolute;
            inset: -20% -20% 0 0;
            pointer-events: none;
            background-image:
                radial-gradient(circle, rgba(255,255,255,0.6) 0 1px, transparent 1px),
                radial-gradient(circle, rgba(255,255,255,0.35) 0 1px, transparent 1px),
                radial-gradient(circle, rgba(255,255,255,0.25) 0 1px, transparent 1px);
            background-size: 140px 140px, 220px 220px, 320px 320px;
            background-position: 0 0, 40px 60px, 80px 120px;
            opacity: 0.7;
            transform: translate3d(0, 0, 0);
            transition: transform 0.1s linear;
        }
        .clouds {
            position: absolute;
            inset: 0;
            pointer-events: none;
            opacity: 0.4;
            z-index: 1;
        }
        .cloud {
            position: absolute;
            font-size: 3rem;
            animation: cloud-drift 45s linear infinite;
            filter: blur(0.3px);
            pointer-events: auto;
            cursor: pointer;
            transition: transform 0.2s ease;
            --dx: 140vw;
            --dy: 0vh;
        }
        .cloud:active {
            transform: scale(0.95);
        }
        .unicorn {
            position: fixed;
            left: 0;
            top: 0;
            transform: translate(-50%, -50%);
            font-size: 1.8rem;
            pointer-events: none;
            will-change: transform, opacity;
            filter: drop-shadow(0 6px 8px rgba(0, 0, 0, 0.35));
            animation: unicorn-fly 1.2s ease-out forwards;
        }
        .glitter {
            position: fixed;
            left: 0;
            top: 0;
            transform: translate(-50%, -50%);
            font-size: 1.1rem;
            pointer-events: none;
            filter: drop-shadow(0 0 6px rgba(255, 255, 255, 0.8));
            animation: glitter-fade 0.8s ease-out forwards;
        }
        .rocket {
            position: fixed;
            left: 0;
            top: 0;
            transform: translate(-50%, -50%);
            font-size: 1.6rem;
            pointer-events: none;
            filter: drop-shadow(0 6px 10px rgba(0, 0, 0, 0.35));
            will-change: transform;
        }
        .corner-cat {
            position: fixed;
            width: 80px;
            height: 80px;
            z-index: 5;
            pointer-events: none;
        }
        .corner-cat .cat {
            font-size: 2.6rem;
            filter: drop-shadow(0 6px 8px rgba(0, 0, 0, 0.35));
        }
        .corner-cat .laser {
            position: absolute;
            left: 50%;
            top: 50%;
            height: 3px;
            width: 220px;
            background: linear-gradient(90deg, rgba(255, 80, 80, 0.0), rgba(255, 80, 80, 0.9) 40%, rgba(255, 200, 200, 1));
            transform-origin: 0 50%;
            filter: drop-shadow(0 0 6px rgba(255, 120, 120, 0.9));
            border-radius: 999px;
        }
        .corner-cat.top-left { left: 12px; top: 12px; }
        .corner-cat.top-right { right: 12px; top: 12px; }
        .corner-cat.bottom-left { left: 12px; bottom: 12px; }
        .corner-cat.bottom-right { right: 12px; bottom: 12px; }
        .corner-cat.top-right .cat,
        .corner-cat.bottom-right .cat {
            transform: scaleX(-1);
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-12px) rotate(-2deg); }
        }
        @keyframes drift {
            0%, 100% { transform: translateY(0); opacity: 0.9; }
            50% { transform: translateY(-14px); opacity: 0.7; }
        }
        @keyframes unicorn-fly {
            0% {
                transform: translate(-50%, -50%) scale(0.7) rotate(-12deg);
                opacity: 0.95;
            }
            100% {
                transform: translate(-50%, calc(-50% - 80px)) scale(1.1) rotate(8deg);
                opacity: 0;
            }
        }
        @keyframes glitter-fade {
            0% { opacity: 1; transform: translate(-50%, -50%) scale(0.9); }
            100% { opacity: 0; transform: translate(-50%, -80%) scale(1.4); }
        }
        @keyframes cloud-drift {
            0% { transform: translate(0, 0); }
            100% { transform: translate(var(--dx), var(--dy)); }
        }
        @keyframes day-night {
            0%, 100% { background: radial-gradient(circle at top, #1f1c2c, #928dab); }
            50% { background: radial-gradient(circle at top, #1a4b7a, #56ccf2); }
        }
    </style>
</head>
<body>
    <div class="stars" aria-hidden="true"></div>
    <div class="sparkles"></div>
    <div class="clouds" aria-hidden="true">
        <div class="cloud">☁️</div>
        <div class="cloud">☁️</div>
        <div class="cloud">☁️</div>
        <div class="cloud">☁️</div>
    </div>
    <div class="card">
        <div class="emoji">🎉</div>
        <h1>Willkommen auf dem Mini‑Webserver!</h1>
        <p>Hab einen wunderbaren Tag — der Server freut sich, dich zu sehen.</p>
        <p>✅ Es hat geklappt: Die Python‑Bibliothek Flask ist installiert und läuft im Docker‑Container auf dem Arduino Uno Q.</p>
    </div>
    <div class="corner-cat top-left" data-eye-x="50" data-eye-y="48">
        <div class="cat">🐱</div>
        <div class="laser"></div>
    </div>
    <div class="corner-cat top-right" data-eye-x="30" data-eye-y="48">
        <div class="cat">🐱</div>
        <div class="laser"></div>
    </div>
    <div class="corner-cat bottom-left" data-eye-x="50" data-eye-y="30">
        <div class="cat">🐱</div>
        <div class="laser"></div>
    </div>
    <div class="corner-cat bottom-right" data-eye-x="30" data-eye-y="30">
        <div class="cat">🐱</div>
        <div class="laser"></div>
    </div>
    <script>
        const unicorns = ["🦄", "🦄", "🦄", "🦄", "🦄", "🦄", "🦄", "🦄", "🦄", "🌈"];
        const glitters = ["✨", "✦", "✧", "⋆"];
        let lastSpawn = 0;

        const cats = Array.from(document.querySelectorAll(".corner-cat"));
        const stars = document.querySelector(".stars");
        const card = document.querySelector(".card");
        const clouds = Array.from(document.querySelectorAll(".cloud"));
        let pointerX = window.innerWidth / 2;
        let pointerY = window.innerHeight / 2;

        function wrapLetters(element) {
            const text = element.textContent ?? "";
            element.textContent = "";
            Array.from(text).forEach((char) => {
                if (char === " ") {
                    element.appendChild(document.createTextNode(" "));
                    return;
                }
                const span = document.createElement("span");
                span.className = "letter";
                span.textContent = char;
                element.appendChild(span);
            });
        }

        [
            ...document.querySelectorAll(".card h1, .card p")
        ].forEach((el) => wrapLetters(el));

        document.querySelectorAll(".letter").forEach((letter) => {
            letter.addEventListener("pointerover", () => {
                const hue = Math.floor(Math.random() * 360);
                letter.style.color = `hsl(${hue}, 90%, 70%)`;
            });
        });

        function randomizeCloud(cloud) {
            const startX = Math.random() * 100;
            const startY = Math.random() * 100;
            const driftAngle = Math.random() * Math.PI * 2;
            const driftDistance = Math.random() * 120 + 60;
            const dx = Math.cos(driftAngle) * driftDistance;
            const dy = Math.sin(driftAngle) * driftDistance * 0.6;
            cloud.style.left = `${startX}vw`;
            cloud.style.top = `${startY}vh`;
            cloud.style.setProperty("--dx", `${dx}vw`);
            cloud.style.setProperty("--dy", `${dy}vh`);
            cloud.style.animationDuration = `${Math.random() * 25 + 35}s`;
            cloud.style.fontSize = `${Math.random() * 1.4 + 2.2}rem`;
        }

        clouds.forEach((cloud) => {
            randomizeCloud(cloud);
            cloud.addEventListener("animationiteration", () => randomizeCloud(cloud));
        });

        function spawnUnicorn(x, y) {
            const unicorn = document.createElement("div");
            unicorn.className = "unicorn";
            unicorn.textContent = unicorns[Math.floor(Math.random() * unicorns.length)];
            unicorn.style.left = `${x}px`;
            unicorn.style.top = `${y}px`;
            unicorn.style.fontSize = `${Math.random() * 0.8 + 1.4}rem`;
            document.body.appendChild(unicorn);

            unicorn.addEventListener("animationend", () => {
                unicorn.remove();
            });
        }

        function spawnGlitter(x, y) {
            const sparkle = document.createElement("div");
            sparkle.className = "glitter";
            sparkle.textContent = glitters[Math.floor(Math.random() * glitters.length)];
            sparkle.style.left = `${x}px`;
            sparkle.style.top = `${y}px`;
            sparkle.style.fontSize = `${Math.random() * 0.6 + 0.8}rem`;
            document.body.appendChild(sparkle);
            sparkle.addEventListener("animationend", () => sparkle.remove());
        }

        function launchRockets(x, y) {
            const count = Math.floor(Math.random() * 3) + 2;
            for (let i = 0; i < count; i += 1) {
                const rocket = document.createElement("div");
                rocket.className = "rocket";
                rocket.textContent = "🚀";
                const offsetX = (Math.random() - 0.5) * 60;
                rocket.style.left = `${x + offsetX}px`;
                rocket.style.top = `${y}px`;
                document.body.appendChild(rocket);

                const startX = x + offsetX;
                const startY = y;
                const speed = Math.random() * 1.5 + 2;
                const drift = Math.random() * 0.4 + 0.6;
                const startTime = performance.now();

                function animateRocket(time) {
                    const elapsed = (time - startTime) / 16.7;
                    const currentY = startY - speed * elapsed * 4;
                    const currentX = startX + drift * elapsed * 10;
                    rocket.style.transform = `translate(-50%, -50%) translate(${currentX - startX}px, ${currentY - startY}px)`;

                    const rocketRect = rocket.getBoundingClientRect();
                    let hit = false;
                    clouds.forEach((cloud) => {
                        if (cloud.textContent === "🍜") return;
                        const cloudRect = cloud.getBoundingClientRect();
                        const overlap = !(
                            rocketRect.right < cloudRect.left ||
                            rocketRect.left > cloudRect.right ||
                            rocketRect.bottom < cloudRect.top ||
                            rocketRect.top > cloudRect.bottom
                        );
                        if (overlap) {
                            cloud.textContent = "🍜";
                            hit = true;
                        }
                    });

                    if (hit || currentY < -60) {
                        rocket.remove();
                        return;
                    }
                    requestAnimationFrame(animateRocket);
                }

                requestAnimationFrame(animateRocket);
            }
        }

        window.addEventListener("pointermove", (event) => {
            const now = performance.now();
            if (now - lastSpawn < 40) return;
            lastSpawn = now;
            spawnUnicorn(event.clientX, event.clientY);
            spawnGlitter(event.clientX, event.clientY);
            pointerX = event.clientX;
            pointerY = event.clientY;
            const offsetX = (event.clientX / window.innerWidth - 0.5) * -20;
            const offsetY = (event.clientY / window.innerHeight - 0.5) * -20;
            if (stars) {
                stars.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
            }
        });

        window.addEventListener("click", (event) => {
            launchRockets(event.clientX, event.clientY);
        });

        clouds.forEach((cloud) => {
            cloud.addEventListener("click", (event) => {
                event.stopPropagation();
                cloud.textContent = "🥙";
            });
        });

        function updateLasers() {
            cats.forEach((cat) => {
                const rect = cat.getBoundingClientRect();
                const eyeX = rect.left + (Number(cat.dataset.eyeX) / 100) * rect.width;
                const eyeY = rect.top + (Number(cat.dataset.eyeY) / 100) * rect.height;
                const dx = pointerX - eyeX;
                const dy = pointerY - eyeY;
                const angle = Math.atan2(dy, dx);
                const distance = Math.min(Math.hypot(dx, dy), 600);
                const laser = cat.querySelector(".laser");
                laser.style.width = `${distance}px`;
                laser.style.transform = `rotate(${angle}rad)`;
            });
            requestAnimationFrame(updateLasers);
        }

        updateLasers();
    </script>
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
