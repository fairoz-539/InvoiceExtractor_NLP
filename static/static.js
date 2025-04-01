document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const fileInput = document.getElementById('invoiceFile');
            const file = fileInput.files[0];
            
            if (!file) {
                document.getElementById('status').innerHTML = '<p class="error-message">Please select a file.</p>';
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('status').innerHTML = '';
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                
                if (response.ok) {
                    document.getElementById('status').innerHTML = '<p class="success-message">Invoice processed and saved successfully!</p>';
                    document.getElementById('result').textContent = JSON.stringify(result, null, 2);
                    loadInvoices(); // Refresh table
                } else {
                    document.getElementById('status').innerHTML = '<p class="error-message">Error: ' + result.error + '</p>';
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('status').innerHTML = '<p class="error-message">Error: ' + error.message + '</p>';
            }
        });
    }

    // Load invoices on page load
    loadInvoices();

    function loadInvoices() {
        fetch('/invoices')
            .then(response => response.json())
            .then(data => {
                const invoicesList = document.getElementById('invoicesList');
                invoicesList.innerHTML = '<h2>Processed Invoices</h2>';
                
                if (!data.invoices || data.invoices.length === 0) {
                    invoicesList.innerHTML += '<p>No invoices processed yet.</p>';
                    return;
                }
                
                const table = document.createElement('table');
                const headerRow = document.createElement('tr');
                const headers = ['Invoice ID', 'Invoice Number', 'Date', 'Total Amount', 'Processed At', 'Actions'];
                headers.forEach(text => {
                    const th = document.createElement('th');
                    th.textContent = text;
                    headerRow.appendChild(th);
                });
                table.appendChild(headerRow);
                
                data.invoices.forEach((invoice, index) => {
                    const row = document.createElement('tr');
                    
                    const cellId = document.createElement('td');
                    cellId.textContent = invoice.invoice_id || 'N/A';
                    row.appendChild(cellId);
                    
                    const cellInvNum = document.createElement('td');
                    cellInvNum.textContent = invoice.invoice_number || 'N/A';
                    row.appendChild(cellInvNum);
                    
                    const cellDate = document.createElement('td');
                    cellDate.textContent = invoice.date || 'N/A';
                    row.appendChild(cellDate);
                    
                    const cellAmount = document.createElement('td');
                    cellAmount.textContent = invoice.total_amount || 'N/A';
                    row.appendChild(cellAmount);
                    
                    const cellProcessed = document.createElement('td');
                    cellProcessed.textContent = invoice.processed_at || 'N/A';
                    row.appendChild(cellProcessed);
                    
                    const cellActions = document.createElement('td');
                    const viewButton = document.createElement('button');
                    viewButton.textContent = 'View';
                    viewButton.addEventListener('click', function() {
                        const itemsForInvoice = data.items.filter(item => item.invoice_id === invoice.invoice_id);
                        const fullData = { ...invoice, items: itemsForInvoice };
                        document.getElementById('result').textContent = JSON.stringify(fullData, null, 2);
                    });
                    cellActions.appendChild(viewButton);
                    row.appendChild(cellActions);
                    
                    table.appendChild(row);
                });
                
                invoicesList.appendChild(table);
            })
            .catch(error => {
                document.getElementById('invoicesList').innerHTML = '<p class="error-message">Error loading invoices: ' + error.message + '</p>';
            });
    }
});