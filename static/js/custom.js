document.addEventListener('DOMContentLoaded', function() {
    const resultsContainer = document.querySelector('.results');
    if (!resultsContainer) return;

    // Create top scrollbar
    const topScrollbar = document.createElement('div');
    topScrollbar.style.overflowX = 'auto';
    topScrollbar.style.overflowY = 'hidden';
    topScrollbar.style.width = '100%';
    topScrollbar.style.height = '20px';
    topScrollbar.style.marginBottom = '5px';

    // Create inner element inside top scrollbar
    const topInner = document.createElement('div');
    const resultsTable = resultsContainer.querySelector('table');
    topInner.style.width = resultsTable.scrollWidth + 'px';
    topInner.style.height = '1px';
    topScrollbar.appendChild(topInner);

    // Insert the top scrollbar before the table
    resultsContainer.parentNode.insertBefore(topScrollbar, resultsContainer);

    // Sync scrolling between top and bottom
    topScrollbar.addEventListener('scroll', function() {
        resultsContainer.scrollLeft = topScrollbar.scrollLeft;
    });
    resultsContainer.addEventListener('scroll', function() {
        topScrollbar.scrollLeft = resultsContainer.scrollLeft;
    });
});
