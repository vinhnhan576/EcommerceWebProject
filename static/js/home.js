const output = document.querySelector(".output");
const outputContainer = document.querySelector(".container");

function resize_to_fit() {
	let fontSize = window.getComputedStyle(output).fontSize;
	output.style.fontSize = parseFloat(fontSize) - 1 + "px";

	if (output.clientHeight >= outputContainer.clientHeight) {
		resize_to_fit();
	}
}

function processInput() {
	output.style.fontSize = "100px"; // Default font size
	resize_to_fit();
}

processInput();
