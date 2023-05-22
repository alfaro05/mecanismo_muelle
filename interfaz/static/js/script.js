const menuBtn = document.getElementById("menu-button");
const menuContent = document.getElementById("dropdown");

const toggleVisibility = function(){
    menuContent.classList.toggle("show-content");
}
menuBtn.addEventListener("click", function (e){
    e.stopPropagation();
    toggleVisibility();
});
document.documentElement.addEventListener("click", function(){
    if(menuContent.classList.contains("show-content")){
        toggleVisibility();
    }
});