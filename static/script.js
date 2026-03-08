const ws = new WebSocket(`ws://${window.location.host}/ws`);
let rec = null;
let active = false;
if ('webkitSpeechRecognition' in window) {
    rec = new webkitSpeechRecognition();
    rec.continuous = true;
    rec.interimResults = false;
    rec.onresult = (e) => {
        const t = e.results[e.results.length - 1][0].transcript;
        document.getElementById('msgIn').value = t;
        send();
    };
}
ws.onmessage = (e) => {
    const d = JSON.parse(e.data);
    const box = document.getElementById('chat');
    const div = document.createElement('div');
    div.style.marginBottom = '8px';
    div.innerHTML = `<b>${d.message.sender}:</b> ${d.message.text}`;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
    document.getElementById('tone').innerText = d.analytics.tone.toUpperCase();
    document.getElementById('sentiment').innerText = d.analytics.sentiment.toUpperCase();
    document.getElementById('intent').innerText = d.analytics.intent;
    const r = document.getElementById('risk');
    r.innerText = d.analytics.escalation_risk.toUpperCase();
    r.className = 'val ' + (d.analytics.escalation_risk === 'high' ? 'high' : '');
};
function send() {
    const i = document.getElementById('msgIn');
    const v = i.value.trim();
    if (v) {
        ws.send(JSON.stringify({ sender: "User", text: v }));
        i.value = '';
    }
}
function toggleRec() {
    if (!rec) return alert("Speech API not supported");
    const b = document.getElementById('recBtn');
    if (active) {
        rec.stop();
        b.innerText = "Record";
        b.classList.remove('rec-active');
    } else {
        rec.start();
        b.innerText = "Listening...";
        b.classList.add('rec-active');
    }
    active = !active;
}
document.getElementById('msgIn').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') send();
});
