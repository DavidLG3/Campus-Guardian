// Test de Autenticación - Campus Guardian
describe('Autenticación de Usuarios', () => {
  let testData
  
  before(() => {
    cy.fixture('testData.json').then((data) => {
      testData = data
    })
  })
  
  beforeEach(() => {
    // Ir directamente al login para evitar el splash screen
    cy.visit('/login')
  })

  describe('Funcionalidad Básica de Auth', () => {
    it('debe mostrar la página de login después del splash', () => {
      cy.url().should('include', '/login')
      cy.get('#email').should('exist')
      cy.get('#password').should('exist')
      cy.get('button[type="submit"]').should('exist')
      cy.contains(/iniciar sesión/i).should('exist')
    })

    it('debe rechazar credenciales incorrectas', () => {
      cy.visit('/login')
      cy.get('#email').type('usuario_incorrecto@test.com')
      cy.get('#password').type('passwordIncorrecto')
      cy.get('button[type="submit"]').click()
      
      // Debería mostrar error y quedarse en login
      cy.wait(2000)
      cy.url().should('include', '/login')
    })

    it('debe iniciar sesión con credenciales de ciudadano', () => {
      cy.visit('/login')
      
      cy.get('#email').type(testData.testUsers.ciudadano.email)
      cy.get('#password').type(testData.testUsers.ciudadano.password)
      cy.get('button[type="submit"]').click()
      
      // Esperar redirección al dashboard
      cy.url({ timeout: 10000 }).should('include', '/dashboard')
      cy.contains(/incidencias/i).should('exist')
    })

    it('debe iniciar sesión con credenciales de admin', () => {
      cy.visit('/login')
      
      cy.get('#email').type(testData.testUsers.admin.email)
      cy.get('#password').type(testData.testUsers.admin.password)
      cy.get('button[type="submit"]').click()
      
      // Admin va a /admin (panel de administración)
      cy.url({ timeout: 10000 }).should('include', '/admin')
    })

    it('debe cerrar sesión correctamente', () => {
      cy.login(testData.testUsers.ciudadano.email, testData.testUsers.ciudadano.password)
      cy.logout()
      cy.url().should('eq', 'http://localhost:5173/')
    })
  })
})
