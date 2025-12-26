import execjs

def exec_js(jscode: str) -> str:
    ctx = execjs.compile("""
        function run_js(jscode) { 
            return eval(jscode); 
        }
""")
    result = ctx.call("run_js", jscode)
    return result
    