// Handle the "Approve" button click
document.querySelectorAll('.btn-approve').forEach(button => {
    button.addEventListener('click', function() {
        if (!this.classList.contains('btn-disabled')) {
            // Update the "Approve" button
            this.textContent = 'Approved';
            this.classList.add('btn-success', 'btn-disabled');
            this.classList.remove('btn-approve');
            
            // Disable both buttons in the same row
            const cancelBtn = this.closest('tr').querySelector('.btn-cancel');
            cancelBtn.classList.add('btn-disabled');
            cancelBtn.disabled = true;
            this.disabled = true;
        }
    });
});

// Handle the "Cancel" button click
document.querySelectorAll('.btn-cancel').forEach(button => {
    button.addEventListener('click', function() {
        if (!this.classList.contains('btn-disabled')) {
            // Update the "Cancel" button
            this.textContent = 'Cancelled';
            this.classList.add('btn-danger', 'btn-disabled');
            this.classList.remove('btn-cancel');
            
            // Disable both buttons in the same row
            const approveBtn = this.closest('tr').querySelector('.btn-approve');
            approveBtn.classList.add('btn-disabled');
            approveBtn.disabled = true;
            this.disabled = true;
        }
    });
});
