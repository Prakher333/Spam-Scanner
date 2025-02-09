document.getElementById("btn").addEventListener("click", async () => {
    document.getElementById("result").innerHTML = ""
    let emailText = document.getElementById("emailText").value;
    if (!emailText.trim()) {
        alert("Please enter a message!");
        return;
    }

    let response = await fetch("https://spam-scanner.onrender.com/predict", {
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
