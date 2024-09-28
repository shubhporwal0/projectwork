document.addEventListener("DOMContentLoaded", function () {
    const detailsButtons = document.querySelectorAll('.details-button');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('close-sidebar');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const jobCards = document.querySelectorAll('.job-list-item');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const sidebarContentInner = document.getElementById('sidebar-content-inner');

    // Error handling if sidebar content inner is not found
    if (!sidebarContentInner) {
        console.error('Sidebar content inner element not found!');
        return;
    }

    // Function to open the sidebar
    function openSidebar() {
        console.log('Opening sidebar');
        sidebar.style.right = '0';
    }

    // Function to close the sidebar
    function closeSidebarFunction() {
        console.log('Closing sidebar');
        sidebar.style.right = '-100%';
        sidebarContentInner.innerHTML = '';  // Clear sidebar content when closed
    }

    // Function to display job details inside sidebar
    function showJobDetails(jobData) {
    console.log('Displaying job details:', jobData);
    
    // Check if long_description is longer than 4000 characters
    let description = jobData.long_description;
    if (description.length > 400) {
        description = description.substring(0, 400) + '...';
    }
    
    sidebarContentInner.innerHTML = `
        <h2 id="sidebar-title">${jobData.title}</h2>
        <h3 id="sidebar-company">${jobData.company_name}</h3>
        <p><strong>Location:</strong> ${jobData.contract_location}</p>
        <p><strong>Work Mode:</strong> ${jobData.work_mode}</p>
        <p><strong>Career Level:</strong> ${jobData.career_level}</p>
        <p><strong>Description:</strong> ${description}</p>
        <a id="sidebar-apply" href="${jobData.application_link}" class="apply-btn">Apply Now</a>
    `;
    openSidebar();  // Open the sidebar after loading job details
}


    // Event listener for the 'Details' and 'Know More' buttons
    detailsButtons.forEach(button => {
        button.addEventListener('click', function () {
            const jobId = this.getAttribute('data-job-id');
            console.log('Fetching details for job ID:', jobId);

            // Check if jobId is valid before making the request
            if (jobId) {
                fetch(`/job-details/${jobId}/`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();  // Parse response JSON
                    })
                    .then(data => {
                        showJobDetails(data);  // Display job details in the sidebar
                    })
                    .catch(error => console.error('Error fetching job details:', error));
            } else {
                console.error('Job ID is missing or invalid!');
            }
        });
    });

    // Close sidebar when the close button is clicked
    closeSidebar.addEventListener('click', closeSidebarFunction);

    // Close sidebar when the user clicks outside of it
    window.addEventListener('click', function (event) {
        if (event.target === sidebar) {
            closeSidebarFunction();
        }
    });

    // Function to filter jobs based on career level
    function filterJobs(careerLevel) {
        jobCards.forEach(card => {
            if (careerLevel === "All" || card.getAttribute('data-career-level') === careerLevel) {
                card.style.display = "flex";
            } else {
                card.style.display = "none";
            }
        });
    }

    // Event listener for filter buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            const filter = this.getAttribute('data-filter');
            console.log('Filtering jobs by career level:', filter);
            filterJobs(filter);
        });
    });

    // Event listener for search button
    searchButton.addEventListener('click', function () {
        const skill = searchInput.value.trim();
        console.log('Searching for skill:', skill);

        if (skill) {
            fetch(`/search/?skill=${encodeURIComponent(skill)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();  // Parse response JSON
                })
                .then(data => {
                    console.log('Search results:', data.jobs);
                    displaySearchResults(data.jobs);
                })
                .catch(error => console.error('Error searching jobs:', error));
        } else {
            console.log('No skill entered');
        }
    });

    // Function to display search results in the sidebar
    function displaySearchResults(jobs) {
        console.log('Displaying search results:', jobs);
        sidebarContentInner.innerHTML = '';  // Clear previous content

        if (jobs.length === 0) {
            sidebarContentInner.innerHTML = '<p>No jobs found matching that skill.</p>';
        } else {
            jobs.forEach(job => {
                const jobElement = document.createElement('div');
                jobElement.classList.add('job-result');
                jobElement.innerHTML = `
                    <h3>${job.title}</h3>
                    <p>${job.company_name}</p>
                    <p><strong>Location:</strong> ${job.contract_location}</p>
                    <p><strong>Career Level:</strong> ${job.career_level}</p>
                    <button class="details-button" data-job-id="${job.job_id}">More Details</button>
                `;

                // Add event listener to display job details when button is clicked
                jobElement.querySelector('.details-button').addEventListener('click', function () {
                    showJobDetails(job);
                });

                sidebarContentInner.appendChild(jobElement);
            });
        }

        openSidebar();  // Ensure the sidebar is opened when displaying search results
    }
});
