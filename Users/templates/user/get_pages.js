var doc = document.getElementById("pg");
function get_pages()
{
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 200) {
			doc.innerHTML = this.responseText;
		}
	};
	xhttp.open("get", "http://127.0.0.1:8000/u/get_pages/", true);
	xhttp.send();
}
window.addEventListener("load", get_pages);
