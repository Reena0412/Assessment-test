from django.http import HttpResponse
from django.shortcuts import render

def accept_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        timeframe = request.POST['timeframe']

        # store the CSV file on the server
        with open('csv_file.csv', 'wb+') as f:
            for chunk in csv_file.chunks():
                f.write(chunk)

        # read the CSV file 
        data = []
        with open('csv_file.csv', 'r') as f:
            for line in f:
                data.append(line.split(','))

        # create a list of candle objects with attributes id, open, high, low, close, date
        candles = []
        for candle in data:
            candles.append({
                'id': candle[0],
                'open': candle[1],
                'high': candle[2],
                'low': candle[3],
                'close': candle[4],
                'date': candle[5]
            })

        # convert the list of candles to the given timeframe using async operations
        # convert the candles to JSON format
        import json
        candles_json = json.dumps(candles)

        # store the JSON data in a file named "candles.json"
        with open('candles.json', 'w') as f:
            f.write(candles_json)

        # provide the user with the option to download the JSON file
        response = HttpResponse(candles_json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="candles.json"'
        return response
    else:
        # render a template page for the user to upload the CSV file and enter the timeframe
        return render(request, 'upload.html')
