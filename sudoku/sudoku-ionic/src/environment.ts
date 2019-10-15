const defaultEnvironment = 'test'
const environment = {
  production: {
    apiUrl: 'https://sudokuic.herokuapp.com',
  },
  test: {
    apiUrl: 'http://localhost:5000',
  }
}

export const environmentVars = environment[defaultEnvironment]