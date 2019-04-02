try {
	var script = document.createElement('script');
	script.src = "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js";
	document.getElementsByTagName('head')[0].appendChild(script);
} catch (error) {
	// Handle import error.
}

function predictWinner() {	
	var red = {
		count: 0,
		mushrooms: 0
	}

	var blue = {
		count: 0,
		mushrooms: 0
	}

	$("span.text-fragment").each(function(element) {
		let msg = this.innerHTML;

		if (msg.includes("!red ") || msg.includes("!blue ")) {
			let split = msg.split(" ");
			let team = split[0].split("!")[1];
			let amount = split[1];
			try {
				amount = parseInt(amount);
				if (!amount) {
					amount = 0;
				}
			} catch (error) {
				amount = 0;
			}

			if (team === "red") {
				red.mushrooms += amount;
			} else if (team === "blue") {
				blue.mushrooms += amount;
			}
		}

		if (msg.includes("!red ")) {
			red.count += 1;
	    } else if (msg.includes("!blue ")) {
			blue.count += 1;
	    }
	});

	console.log("Blue: \t" + blue.mushrooms + " mushrooms with " + blue.count + " bets. \nRed: \t" + red.mushrooms + " mushrooms with " + red.count + " bets.");

	if (red.count + blue.count < 15) {
		return "Voting is closed.";
	}

	if (red.count > blue.count) {
		return "red";
	}

	return "blue";
}

function winnerSelected() {
	let win = window.open("https://ytroulette.com/?i=899&c=1");
	win.focus();
}

var interval = setInterval(function() { 
	let winner = predictWinner();

	if (winner === "red" || winner === "blue") {
		// clearInterval(interval);
		// winnerSelected();
		// alert("The winner is: " + winner);
	}
}, 10000);
