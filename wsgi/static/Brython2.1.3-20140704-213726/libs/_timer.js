var $module = (function($B){

    var __builtins__ = $B.builtins
    
    function wrap(func){
        // Transforms a function f into another function that prints a
        // traceback in case of exception
        return function(){
            try{return func.apply(null,arguments)}
            catch(err){
                var exc = $B.exception(err)
                var w = $B.builtins.getattr($B.stderr,'write')
                w(exc.info)
                w('\n'+exc.__name__)
                if(exc.message){w(': '+exc.message)}
                w('\n')
            }
        }
    }
    
    return {

        __name__ : 'timer',
    
        clear_interval : function(int_id){window.clearInterval(int_id)},
        
        clear_timeout : function(timeout_id){window.clearTimeout(timeout_id)},
    
        set_interval : function(func,interval){
            return __builtins__.int(window.setInterval(wrap(func),interval))
        },
    
        set_timeout : function(func,interval){
            return __builtins__.int(window.setTimeout(wrap(func),interval))
        },
        
        request_animation_frame: function(func){
            return __builtins__.int(window.requestAnimationFrame(func))},
        
        cancel_animation_frame: function(int_id){window.cancelAnimationFrame(int_id)}
    }

})(__BRYTHON__)
