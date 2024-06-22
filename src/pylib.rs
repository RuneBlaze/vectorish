use std::sync::Arc;

use pyo3::prelude::*;
use pyo3::types::PyIterator;
use pyo3::{PyAny, PyObject};
use skiplist::{skiplist::Iter, SkipList};

#[pyclass]
pub struct Vectorish {
    pub inner: SkipList<PyObject>,
}

#[pymethods]
impl Vectorish {
    #[new]
    fn new() -> Self {
        Vectorish {
            inner: SkipList::new(),
        }
    }

    fn append(&mut self, item: PyObject) {
        self.inner.push_back(item);
    }

    fn append_left(&mut self, item: PyObject) {
        self.inner.push_front(item);
    }

    fn pop(&mut self, i: Option<usize>) -> PyResult<PyObject> {
        match i {
            Some(i) => {
                if i < self.inner.len() {
                    Ok(self.inner.remove(i))
                } else {
                    Err(pyo3::exceptions::PyIndexError::new_err(
                        "index out of range",
                    ))
                }
            }
            None => {
                if self.inner.len() > 0 {
                    Ok(self.inner.pop_back().unwrap())
                } else {
                    Err(pyo3::exceptions::PyIndexError::new_err(
                        "pop from empty list",
                    ))
                }
            }
        }
    }

    fn __len__(&self) -> usize {
        self.inner.len()
    }

    fn insert(&mut self, index: usize, item: PyObject) {
        if index < self.inner.len() {
            self.inner.insert(item, index);
        } else {
            self.inner.push_back(item);
        }
    }

    fn __getitem__(&self, index: isize) -> PyResult<PyObject> {
        if index < 0 {
            let index = self.inner.len() as isize + index;
            match self.inner.get(index as usize) {
                Some(item) => Ok(item.clone()),
                None => Err(pyo3::exceptions::PyIndexError::new_err(
                    "index out of range",
                )),
            }
        } else {
            match self.inner.get(index as usize) {
                Some(item) => Ok(item.clone()),
                None => Err(pyo3::exceptions::PyIndexError::new_err(
                    "index out of range",
                )),
            }
        }
    }

    fn __setitem__(&mut self, index: isize, item: PyObject) -> PyResult<()> {
        if index < 0 {
            let index = self.inner.len() as isize + index;
            match self.inner.get_mut(index as usize) {
                Some(old_item) => {
                    *old_item = item;
                    Ok(())
                }
                None => Err(pyo3::exceptions::PyIndexError::new_err(
                    "index out of range",
                )),
            }
        } else {
            match self.inner.get_mut(index as usize) {
                Some(old_item) => {
                    *old_item = item;
                    Ok(())
                }
                None => Err(pyo3::exceptions::PyIndexError::new_err(
                    "index out of range",
                )),
            }
        }
    }

    fn clear(&mut self) {
        self.inner.clear();
    }

    fn reverse(&mut self) {
        self.inner = self.inner.iter().rev().cloned().collect();
    }

    fn __repr__(&self) -> String {
        format!("vector([{}])", self.inner.iter().map(|x| x.to_string()).collect::<Vec<String>>().join(", "))
    }

    fn __str__(&self) -> String {
        self.__repr__()
    }
}