import uvicorn
from app import main



if __name__ == '__main__':
    # Used to debug via pycharm configuration. Run a python script here and it will allow for reloading and debugging
    main.main()
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000, debug=True)
