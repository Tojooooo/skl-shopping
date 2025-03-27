document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll(".button-comment");
    var modal = document.getElementById("comment-modal");
    var closeButton = document.querySelector(".close-btn");
    var commentSection = document.getElementById("comment-section");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            var productId = button.getAttribute("product");

            fetch(`/get-comments/${productId}/`)  // Endpoint Django pour récupérer les commentaires
                .then(response => response.json())
                .then(data => {
                    displayComments(data.comments);
                    modal.style.display = "flex";
                })
                .catch(error => console.error("Erreur lors de la récupération des commentaires :", error));
        });
    });
    closeButton.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Fermer la modale lorsqu'on clique en dehors du contenu
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    function displayComments(comments) {
        commentSection.innerHTML = ""; // Vider avant d'ajouter les nouveaux commentaires

        if (comments.length === 0) {
            commentSection.innerHTML = "<p>Aucun commentaire disponible.</p>";
            return;
        }

        comments.forEach(comment => {
            var commentDiv = document.createElement("div");
            commentDiv.classList.add("comment");
            commentDiv.innerHTML = `<strong>${comment.username}</strong>: ${comment.text}`;
            commentSection.appendChild(commentDiv);
        });
    }

});


