import pickle   

with open('model.bin', 'rb') as f_in:
    cv, tfidf, model = pickle.load(f_in)

def predict(url):
    X = cv.transform([url])
    X = tfidf.transform(X)
    y_pred = model.predict(X)
    y_pred = y_pred[0].tolist()
    return y_pred

def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result

