function downloadPDF(name, pf_number) {
    const content = document.getElementById('clock');
    html2canvas(content, {
        scale: 2  // Increase the scale for better resolution
    }).then(canvas => {
        const imgData = canvas.toDataURL('image/png');
        const { jsPDF } = window.jspdf;
        // Create a new jsPDF instance with desired page dimensions
        const pdf = new jsPDF({
            orientation: 'portrait',
            unit: 'pt',
            format: 'a4'
        });
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = pdf.internal.pageSize.getHeight();
        // Calculate the width and height to maintain aspect ratio
        const imgWidth = pdfWidth - 20;  // Leave some margin
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        // Check if the image height exceeds PDF height
        if (imgHeight > pdfHeight) {
            const scaleFactor = pdfHeight / imgHeight;
            pdf.addImage(imgData, 'PNG', 10, 10, imgWidth * scaleFactor, pdfHeight - 20);
        } else {
            pdf.addImage(imgData, 'PNG', 10, 10, imgWidth, imgHeight);
        }
        const fileName = `${name}-${pf_number}.pdf`;
        pdf.save(fileName);
    }).catch(error => {
        console.error('Failed', error);
    });
}



