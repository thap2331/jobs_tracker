// Create function to display/hide tabs
function openTab(evt, tabName) {
    var i, tabContent, tabButtons;
    
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }

    tabButtons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabButtons.length; i++) {
        tabButtons[i].className = tabButtons[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
};

// Generate tables
// searchTableHead = ['Company Name', 'Job Listings Link', 'Job Title']
// resultsTableHead = ['Job Link', 'Job Title', 'Company Job Listings Link', 'Source', 'Notified']