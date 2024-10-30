// when all dom is loaded, this will execute, this is basically for toggling between dark and light mode
document.addEventListener("DOMContentLoaded", function () {
    const buttonelement = document.getElementById("toggle-button")
    const logoimageelement = document.getElementById("logo")
    const defaultTheme = localStorage.getItem('theme') || 'dark'; // browsers have this, if not present, set default as dark

    document.documentElement.setAttribute('data-theme', defaultTheme);
    // since I havent defined any css related to data-theme for dark, it will use the dault ^
    // document.documentElement is a way to access the <html> tag (root element)

    if (defaultTheme === 'light') {
        buttonelement.src = '/static/suntheme.png';
        logoimageelement.src ='/static/logo-dark.svg'
    } else {
        buttonelement.src = '/static/moontheme.png';
        logoimageelement.src ='/static/logo-light.svg'
    }
    // upper part is basically like a get request, this is what the user sees whenever he comes to the page, even if its a reload
    // below part is the actual logic for changing the colors
    buttonelement.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme'); // for this logic, we first get the current theme 
        // which is in the html element (document.documentElement)
        if (currentTheme === 'dark')
        {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            buttonelement.src = '/static/suntheme.png';
            logoimageelement.src ='/static/logo-dark.svg';        
        }
        else
        {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            buttonelement.src = '/static/moontheme.png';
            logoimageelement.src ='/static/logo-light.svg';
        }
    })
})
/*
The element pen-icon (the image) acts like a button as when clicked, with the help of javascript.
When clicked, the button then calls for the input element (with the file type and file name),
Then fileInput.click() simulates a click on the input (button) opening up the users file system.
For reference:
This input is normally a button which the user can click (Choose file button), but we hide this from the user.
*/
document.addEventListener("DOMContentLoaded", function () {
    const penIcon = document.getElementById('pen-icon');
    const fileInput = document.getElementById('file');

    penIcon.addEventListener('click', function() {
        fileInput.click(); 
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const filterButton = document.querySelector(".filter-button");
    const filterDropdown = document.querySelector('.filter-dropdown');
    const filterSelect = document.querySelector(".filter-select");
    const filterText = document.querySelector(".filter-text"); 

    filterButton.addEventListener("click", ()=> { 
        filterDropdown.classList.toggle('show'); // if there is a click on the button, 
        // if the class is not there, its added, and its its there, it is removed
    });
    // the below code make sures that the same as the remove show class happens, but when the user clicks anywhere else on the page
    document.addEventListener('click', function(e) {
        if (!filterButton.contains(e.target) && !filterDropdown.contains(e.target)) { /* the code checks if this clicked element 
            (e.target) is outside both the filterButton and filterDropdown */
            filterDropdown.classList.remove('show');
        }
    });

    filterSelect.addEventListener("change", (e) => {
        filterText.textContent = e.target.value.charAt(0).toUpperCase() + e.target.value.slice(1); 
        // Capitalize the first letter of the value in the option selected eg- value="interests" becomes I+nterest = Interest
        filterDropdown.classList.remove('show'); // Close the dropdown after selection
    });
});