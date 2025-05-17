document.addEventListener('DOMContentLoaded', function () {
    const openSearchModalBtn = document.getElementById('openSearchModalBtn');
    const closeSearchModalBtn = document.getElementById('closeSearchModalBtn');
    const searchModal = document.getElementById('searchModal');
    const modalSearchInput = document.getElementById('modalSearchInput');
    const dynamicSearchResultsContainer = document.getElementById('dynamicSearchResults');
    const modalSearchForm = document.getElementById('modalSearchForm'); // Get the form

    let debounceTimer;

    function openModal() {
        if (searchModal) {
            searchModal.classList.remove('modal-hidden');
            document.body.classList.add('overflow-hidden');
            setTimeout(() => {
                searchModal.classList.remove('opacity-0', 'pointer-events-none');
                searchModal.querySelector('.modal-content').classList.remove('scale-95', 'opacity-0');
                
                if (modalSearchInput) {
                    modalSearchInput.value = ''; // Clear the input field
                    modalSearchInput.focus();
                }
                if (dynamicSearchResultsContainer) {
                     dynamicSearchResultsContainer.innerHTML = '<p class="text-gray-500 text-center py-4">Start typing to see results.</p>';
                }
            }, 20);
        }
    }

    function closeModal() {
        if (searchModal) {
            searchModal.classList.add('opacity-0', 'pointer-events-none');
            searchModal.querySelector('.modal-content').classList.add('scale-95', 'opacity-0');
            setTimeout(() => {
                searchModal.classList.add('modal-hidden');
                document.body.classList.remove('overflow-hidden');
            }, 300);
        }
    }

    async function fetchDynamicResults() {
        const query = modalSearchInput.value.trim();
        if (dynamicSearchResultsContainer) dynamicSearchResultsContainer.innerHTML = ''; // Clear previous results

        if (query.length < 2) { // Only search if query is 2+ chars
            if (dynamicSearchResultsContainer) dynamicSearchResultsContainer.innerHTML = '<p class="text-gray-500 text-center py-4">Please type at least 2 characters.</p>';
            return;
        }

        if (dynamicSearchResultsContainer) dynamicSearchResultsContainer.innerHTML = '<p class="text-gray-500 text-center py-4">Searching...</p>';

        try {
            // IMPORTANT: Replace with the actual URL name if it's different or if you need to generate it dynamically in Django template first
            const response = await fetch(`/search/api/dynamic-group-search/?query=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (dynamicSearchResultsContainer) {
                if (data.groups && data.groups.length > 0) {
                    data.groups.forEach(group => {
                        const resultItem = document.createElement('a');
                        resultItem.href = group.url; // Placeholder URL from API
                        resultItem.className = 'block p-3 bg-gray-50 hover:bg-indigo-100 rounded-md transition';
                        resultItem.innerHTML = `
                            <h4 class="font-semibold text-indigo-700">${escapeHTML(group.name)}</h4>
                            ${group.description ? `<p class="text-sm text-gray-600 truncate">${escapeHTML(group.description)}</p>` : ''}
                            <p class="text-xs text-gray-400 mt-1">
                                Focus: ${escapeHTML(group.content_focus_title)} | By: @${escapeHTML(group.creator_username)}
                            </p>
                        `;
                        // If user clicks a dynamic result, redirect them (or could fill search and submit main form)
                        resultItem.addEventListener('click', function(e) {
                            e.preventDefault(); // Prevent default link behavior for now
                            // Option 1: Go to the group page directly (if URL is valid)
                            // window.location.href = group.url;

                            // Option 2: Fill the main search form and submit it to the full results page
                            if(modalSearchForm) {
                                modalSearchInput.value = group.name; // Or the original query that found this
                                modalSearchForm.submit();
                            }
                        });
                        dynamicSearchResultsContainer.appendChild(resultItem);
                    });
                } else {
                    dynamicSearchResultsContainer.innerHTML = '<p class="text-gray-500 text-center py-4">No groups found matching your query.</p>';
                }
            }
        } catch (error) {
            console.error("Error fetching dynamic search results:", error);
            if (dynamicSearchResultsContainer) dynamicSearchResultsContainer.innerHTML = '<p class="text-red-500 text-center py-4">Could not load search results. Please try again.</p>';
        }
    }

    // Helper to escape HTML to prevent XSS if data isn't already sanitized
    function escapeHTML(str) {
        const div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    if (openSearchModalBtn) openSearchModalBtn.addEventListener('click', openModal);
    if (closeSearchModalBtn) closeSearchModalBtn.addEventListener('click', closeModal);
    
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !searchModal.classList.contains('modal-hidden')) closeModal();
    });
    
    if (searchModal) {
        searchModal.addEventListener('click', function(event) {
            if (event.target === searchModal) closeModal();
        });
    }

    if (modalSearchInput) {
        modalSearchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(fetchDynamicResults, 500); // Debounce for 500ms
        });
    }
}); 