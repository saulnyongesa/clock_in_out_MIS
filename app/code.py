def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def generate_pdf(request):
    trainers = TrainerUnit.objects.all()

    # Group TrainerUnits by Trainer
    trainers_grouped = {}
    for trainer_unit in trainers:
        trainer = trainer_unit.trainer
        if trainer not in trainers_grouped:
            trainers_grouped[trainer] = []
        trainers_grouped[trainer].append(trainer_unit.unit.unit_name)
        trainers_grouped[trainer].append(trainer_unit.unit.unit_code)

    # Prepare data for PDF generation
    data = [("Name", "PF/ID No.", "Unit")]  # Sample header row
    for trainer, units in trainers_grouped.items():
        for unit in units:
            data.append((trainer.name, trainer.pf_number, unit))

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;' + 'filename=' + "Trainers-" + f"{str(t2.now())}.pdf"
    c = canvas.Canvas(response, pagesize=landscape(A4))  # Landscape orientation
    w, h = landscape(A4)
    max_rows_per_page = 40
    x_offset = 5
    y_offset = 5
    padding = 5
    xlist = [x + x_offset for x in [0, 250, 350, 700, 800]]  # Adjust column positions as needed
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()

    c.save()

    return response
