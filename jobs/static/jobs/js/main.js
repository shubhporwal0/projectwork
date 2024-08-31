document.addEventListener("DOMContentLoaded", function () {
    const detailsButtons = document.querySelectorAll('.details-button');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('close-sidebar');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const jobCards = document.querySelectorAll('.job-list-item');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const sidebarContentInner = document.getElementById('sidebar-content-inner');

    if (!sidebarContentInner) {
        console.error('Sidebar content inner element not found!');
        return;
    }

    function openSidebar() {
        console.log('Opening sidebar');
        sidebar.style.right = '0';
    }

    function closeSidebarFunction() {
        console.log('Closing sidebar');
        sidebar.style.right = '-100%';
        sidebarContentInner.innerHTML = ''; // Clear the sidebar content when closing
    }

    function showJobDetails(jobData) {
        console.log('Displaying job details:', jobData);
        sidebarContentInner.innerHTML = `
            <h2 id="sidebar-title">${jobData.title}</h2>
            <h3 id="sidebar-company">${jobData.company_name}</h3>
            <p><strong>Location:</strong> ${jobData.contract_location}</p>
            <p><strong>Work Mode:</strong> ${jobData.work_mode}</p>
            <p><strong>Career Level:</strong> ${jobData.career_level}</p>
            <p><strong>Description:</strong> ${jobData.long_description}</p>
            <a id="sidebar-apply" href="${jobData.application_link}" class="apply-btn">Apply Now</a>
        `;
        openSidebar();
    }

    detailsButtons.forEach(button => {
        button.addEventListener('click', function () {
            const jobId = this.getAttribute('data-job-id');
            console.log('Fetching details for job ID:', jobId);

            fetch(`/job-details/${jobId}/`)
                .then(response => response.json())
                .then(data => {
                    showJobDetails(data);
                })
                .catch(error => console.error('Error fetching job details:', error));
        });
    });

    closeSidebar.addEventListener('click', closeSidebarFunction);

    window.addEventListener('click', function (event) {
        if (event.target === sidebar) {
            closeSidebarFunction();
        }
    });

    function filterJobs(careerLevel) {
        jobCards.forEach(card => {
            if (careerLevel === "All" || card.getAttribute('data-career-level') === careerLevel) {
                card.style.display = "flex";
            } else {
                card.style.display = "none";
            }
        });
    }

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            const filter = this.getAttribute('data-filter');
            console.log('Filtering jobs by career level:', filter); // Debugging log
            filterJobs(filter);
        });
    });

    searchButton.addEventListener('click', function () {
        const skill = searchInput.value.trim();
        console.log('Searching for skill:', skill);

        if (skill) {
            fetch(`/search/?skill=${encodeURIComponent(skill)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
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

    function displaySearchResults(jobs) {
        console.log('Displaying search results:', jobs);
        sidebarContentInner.innerHTML = ''; // Clear previous content

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
                    <button class="details-button" data-job-id="${job.id}">More Details</button>
                `;

                jobElement.querySelector('.details-button').addEventListener('click', function () {
                    showJobDetails(job);
                });

                sidebarContentInner.appendChild(jobElement);
            });
        }

        openSidebar(); // Ensure the sidebar is opened
    }
});
