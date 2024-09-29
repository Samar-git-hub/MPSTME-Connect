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