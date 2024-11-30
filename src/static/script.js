// script.js
document.getElementById("start-convo").onclick = async () => {
    const topic = document.getElementById("topic-input").value;
    
    const response = await fetch("/start_conversation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ topic: topic })
    });
    
    const result = await response.json();
    console.log(result.message);  // Confirm the AI started learning about the topic
};
