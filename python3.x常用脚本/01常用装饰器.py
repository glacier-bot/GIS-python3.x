##try-except装饰器
def try_it(f):
    import sys
    import traceback
    def handle(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except Exception:
            exc_type,exc_instance,exc_traceback=sys.exc_info()
            formatted_traceback="".join(traceback.format_tb(exc_traceback))
            message="\n{0}\n{1}:\n{2}".format(
                formatted_traceback,
                exc_type.__name__,
                exc_instance
            )
            print(exc_type(message))
        finally:
            pass
    return handle

##计时装饰器
def time_it(f):
    import time
    def handle(*args,**kwargs):
        start=time.time()
        result=f(*args,**kwargs)
        end=time.time()
        print("Time elapsed: ",end-start)
        return result
    return handle

if __name__ == "__main__":
    @try_it
    def test_error():
        return 1+""

    @time_it
    def test_time():
        for i in range(1):
            print(i)
    
    test_error()
    test_time()