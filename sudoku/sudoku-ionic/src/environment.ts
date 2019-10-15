const defaultEnvironment = 'production'
const environment = {
  production: {
    apiUrl: 'https://sa-sudoku-solver.herokuapp.com',
  },
  test: {
    apiUrl: 'http://localhost:5000',
  }
}

export const environmentVars = environment[defaultEnvironment]
