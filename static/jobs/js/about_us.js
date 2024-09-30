document.addEventListener('DOMContentLoaded', function () {
    const teamMembers = document.querySelectorAll('.team-member');
    const boxes = document.querySelectorAll('.mission-box, .value-box');

    // Hover effect for team members
    teamMembers.forEach(member => {
        member.addEventListener('mouseover', function () {
            this.style.transform = 'scale(1.15)';
            this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.15)';
        });
        member.addEventListener('mouseout', function () {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.1)';
        });
    });

    // Hover effect for mission and value boxes
    boxes.forEach(box => {
        box.addEventListener('mouseover', function () {
            this.style.transform = 'scale(1.1)';
            this.style.boxShadow = '0 12px 20px rgba(0, 0, 0, 0.15)';
            this.style.backgroundColor = '#E1F5FE'; // Light highlight on hover
        });
        box.addEventListener('mouseout', function () {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.1)';
            this.style.backgroundColor = '#fff'; // Revert background
        });
    });
});
