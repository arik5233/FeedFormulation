from website import create_app

app = create_app()
app.run()
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)