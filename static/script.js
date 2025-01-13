// when all dom is loaded, this will execute, this is basically for toggling between dark and light mode
document.addEventListener("DOMContentLoaded", function () {
    const buttonelement = document.getElementById("toggle-button");
    const hamburgermenu = document.getElementById("hamburger-icon");
    const logoimageelement = document.getElementById("logo");
    const profileindex = document.getElementById("profile-page-index");
    const searchindex = document.getElementById("search-page-index");
    const events1index = document.getElementById("events-1-page-index");
    const events2index = document.getElementById("events-2-page-index");
    const event1 = document.getElementById("event-1");
    const event2 = document.getElementById("event-2");
    const event3 = document.getElementById("event-3");
    const verifylogo = document.getElementById("verify-logo");
    const defaultTheme = localStorage.getItem('theme') || 'dark'; // browsers have this, if not present, set default as dark

    document.documentElement.setAttribute('data-theme', defaultTheme);
    // since I havent defined any css related to data-theme for dark, it will use the default ^
    // document.documentElement is a way to access the <html> tag (root element)

    if (defaultTheme === 'light') {
        buttonelement.src = '/static/suntheme.png';
        hamburgermenu && (hamburgermenu.src = '/static/hamburger-light.png');
        logoimageelement && (logoimageelement.src = '/static/logo-light.svg');
        profileindex && (profileindex.src = '/static/profilepage-index-light.png');
        searchindex && (searchindex.src = '/static/searchpage-index-light.png');
        events1index && (events1index.src = '/static/eventspage-index-1-light.png');
        events2index && (events2index.src = '/static/eventspage-index-2-light.png');
        event1 && (event1.src = '/static/mumbaimunlogo-light.png');
        event2 && (event2.src = '/static/socialconclavelogo-light.png');
        event3 && (event3.src = '/static/taqneeqlogo-light.png');
        verifylogo && (verifylogo.src = '/static/logo-light.svg');
    } else {
        buttonelement.src = '/static/moontheme.png';
        hamburgermenu && (hamburgermenu.src = '/static/hamburger-dark.png');
        logoimageelement && (logoimageelement.src = '/static/logo-dark.svg');
        profileindex && (profileindex.src = '/static/profilepage-index.png');
        searchindex && (searchindex.src = '/static/searchpage-index.png');
        events1index && (events1index.src = '/static/eventspage-index-1.png');
        events2index && (events2index.src = '/static/eventspage-index-2.png');
        event1 && (event1.src = '/static/mumbaimunlogo.jpg');
        event2 && (event2.src = '/static/socialconclavelogo.png');
        event3 && (event3.src = '/static/taqneeqlogo.jpg');
        verifylogo && (verifylogo.src = '/static/logo-dark.svg');
    }
    // upper part is basically like a get request, this is what the user sees whenever he comes to the page, even if its a reload
    // below part is the actual logic for changing the colors
    buttonelement.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme'); // for this logic, we first get the current theme 
        // which is in the html element (document.documentElement)
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            buttonelement.src = '/static/suntheme.png';
            hamburgermenu && (hamburgermenu.src = '/static/hamburger-light.png');
            logoimageelement && (logoimageelement.src = '/static/logo-light.svg');
            profileindex && (profileindex.src = '/static/profilepage-index-light.png');
            searchindex && (searchindex.src = '/static/searchpage-index-light.png');
            events1index && (events1index.src = '/static/eventspage-index-1-light.png');
            events2index && (events2index.src = '/static/eventspage-index-2-light.png');
            event1 && (event1.src = '/static/mumbaimunlogo-light.png');
            event2 && (event2.src = '/static/socialconclavelogo-light.png');
            event3 && (event3.src = '/static/taqneeqlogo-light.png');
            verifylogo && (verifylogo.src = '/static/logo-light.svg');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            buttonelement.src = '/static/moontheme.png';
            hamburgermenu && (hamburgermenu.src = '/static/hamburger-dark.png');
            logoimageelement && (logoimageelement.src = '/static/logo-dark.svg');
            profileindex && (profileindex.src = '/static/profilepage-index.png');
            searchindex && (searchindex.src = '/static/searchpage-index.png');
            events1index && (events1index.src = '/static/eventspage-index-1.png');
            events2index && (events2index.src = '/static/eventspage-index-2.png');
            event1 && (event1.src = '/static/mumbaimunlogo.jpg');
            event2 && (event2.src = '/static/socialconclavelogo.png');
            event3 && (event3.src = '/static/taqneeqlogo.jpg');
            verifylogo && (verifylogo.src = '/static/logo-dark.svg');
        }
    });
});

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

document.addEventListener("DOMContentLoaded", ()=> {
    const filterSelect = document.querySelector(".filter-select");
    const searchInput = document.querySelector(".search-inputbox");
    const filterForm = filterSelect.closest('form');

    function searchProfiles() {
        const filterValue = filterSelect.value; //current value of filter
        const searchItem = searchInput.value.toLowerCase();
        const profilePreviews = document.querySelectorAll(".profile-preview");
        // the querySelectorAll returns a NodeList is specifically a collection of DOM nodes (elements in the HTML document)

        profilePreviews.forEach(profile => {
            let targetText;
            console.log("Filter value: ", filterValue);
            if (filterValue === 'Name') {
                targetText = profile.querySelector(".search-name").textContent; // if the filterValue is name, then search by the 
                // javascript querySelector will return the element with ".search-name" class, eg - <div class="search-name">Jamal Kamlesh</div>
                // and then the TextContent returns Jamal Kamlesh (the text inside the element) as raw text, not in a list or something.
            } 
            else {
                targetText = profile.querySelector(".search-description").textContent;
                // any other option, and we are searching in the description part instead of the name part
            }

            const finalText = targetText.toLowerCase(); // convert this text to lowercase
            
            if (!finalText.includes(searchItem)) { // check if the text entered by the user has the text in the elements
                profile.style.display = "none"; // if its not there, dont display the profile 
            }
            else {
                profile.style.display = ""; // if its there display with default css styles
            }
        });
    }

    filterSelect.addEventListener("change", () => { // if the user chooses a different option,
        // call the search function, as in the display should be changed
        searchProfiles();
        filterForm.submit();
    });
    searchInput.addEventListener("input", () => { // do the same normally if the input is changed
        searchProfiles();
    });    
});