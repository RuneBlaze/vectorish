pub mod pylib;
use pyo3::prelude::*;

// /// Formats the sum of two numbers as string.
// #[pyfunction]
// fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
//     Ok((a + b).to_string())
// }

/// A Python module implemented in Rust.
#[pymodule]
fn vectorish(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<pylib::Vectorish>()?;
    Ok(())
}
