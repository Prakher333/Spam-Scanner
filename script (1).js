document.getElementById("btn").addEventListener("click", async () => {
    let emailText = document.getElementById("emailText").value;
    if (!emailText.trim()) {
        alert("Please enter a message!");
        return;
    }

    let response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: emailText }),
    });

    let result = await response.json();
    console.log(result)
    console.log("prediction: ", result.prediction)
    document.getElementById("result").innerHTML = `<h2>${result.prediction}</h2>`

    if(result.prediction != "Spam"){
        document.getElementById("result").style.color = "green";
    }
});