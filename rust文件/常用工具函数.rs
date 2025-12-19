/// 接受一个可调用对象（函数/闭包），但不执行它，直接返回该可调用对象
fn skip<F, R>(f: F) -> F
where
    F: Fn() -> R,
{
    f
}

/// 含2个参数版本，n个参数可以依此类推
fn skip_with_one_arg<F, A, R>(f: F) -> F
where
    F: Fn(A) -> R,
{
    f
}

/// 宏版本，不进行类型检查，但是更灵活
macro_rules! skip {
    ($f:expr) => {
        $f
    };
}
