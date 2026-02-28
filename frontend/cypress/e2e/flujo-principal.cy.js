// Test de Flujo Principal E2E - Campus Guardian
// Este test demuestra el flujo completo de la aplicación

describe('Flujo Principal E2E - Campus Guardian', () => {
  let testData
  let testTimestamp = Date.now()

  before(() => {
    cy.fixture('testData.json').then((data) => {
      testData = data
    })
  })

  describe('Flujo 1: Usuario Ciudadano - Reportar Incidencia', () => {
    beforeEach(() => {
      // Mantener sesión entre tests del mismo flujo
      cy.login(testData.testUsers.ciudadano.email, testData.testUsers.ciudadano.password)
    })

    it('debe reportar una nueva incidencia completa', () => {
      // Navegar a crear incidencia
      cy.visit('/incidencias/nueva')
      cy.url().should('include', '/incidencias/nueva')
      
      // Llenar formulario
      const descripcion = `TEST-Robo-${testTimestamp}: Incidencia de prueba E2E`
      
      cy.get('#tipo').select('robo')
      cy.get('#descripcion').type(descripcion)
      cy.get('#incidencia-map', { timeout: 5000 }).should('be.visible')
      cy.get('#incidencia-map').click('center')
      cy.get('#direccion').type('Biblioteca Central UAM')
      
      // Enviar
      cy.get('button[type="submit"]').click()
      cy.wait(3000)
      cy.url({ timeout: 10000 }).should('not.include', '/nueva')
    })

    it('debe ver la incidencia en su listado', () => {
      cy.visit('/mis-incidencias')
      cy.wait(2000)
      cy.get('body').should('contain.text', `TEST-Robo-${testTimestamp}`)
    })

    it('debe ver el mapa de incidencias', () => {
      cy.visit('/mapa')
      cy.get('.leaflet-container', { timeout: 10000 }).should('exist')
    })
  })

  describe('Flujo 2: Administrador - Gestión de Incidencias', () => {
    beforeEach(() => {
      cy.logout()
      cy.login(testData.testUsers.admin.email, testData.testUsers.admin.password)
    })

    it('debe ver el listado de incidencias', () => {
      cy.visit('/incidencias')
      cy.wait(2000)
      cy.get('body').should('contain.text', `TEST-Robo-${testTimestamp}`)
    })

    it('debe abrir el detalle de una incidencia', () => {
      cy.visit('/incidencias')
      cy.wait(2000)
      cy.contains('.incidencia-card', `TEST-Robo-${testTimestamp}`)
        .find('.btn-view')
        .click()
      cy.url({ timeout: 5000 }).should('match', /\/incidencias\/\d+/)
    })

    it('debe ver el mapa de incidencias', () => {
      cy.visit('/mapa')
      cy.get('.leaflet-container', { timeout: 10000 }).should('exist')
    })
  })

  describe('Flujo 3: Operador de Seguridad - Revisión', () => {
    beforeEach(() => {
      cy.logout()
      cy.login(testData.testUsers.operador.email, testData.testUsers.operador.password)
    })

    it('debe ver el listado de incidencias', () => {
      cy.visit('/incidencias')
      cy.wait(2000)
      cy.get('body').should('contain.text', `TEST-Robo-${testTimestamp}`)
    })

    it('debe abrir el detalle de una incidencia', () => {
      cy.visit('/incidencias')
      cy.wait(2000)
      cy.contains('.incidencia-card', `TEST-Robo-${testTimestamp}`)
        .find('.btn-view')
        .click()
      cy.url({ timeout: 5000 }).should('match', /\/incidencias\/\d+/)
    })

    it('debe ver el mapa de incidencias', () => {
      cy.visit('/mapa')
      cy.get('.leaflet-container', { timeout: 10000 }).should('exist')
    })
  })

  describe('Flujo 4: Verificación Final', () => {
    beforeEach(() => {
      cy.logout()
      cy.login(testData.testUsers.ciudadano.email, testData.testUsers.ciudadano.password)
    })

    it('debe ver el estado de su incidencia', () => {
      cy.visit('/mis-incidencias')
      cy.wait(2000)
      cy.get('body').should('contain.text', `TEST-Robo-${testTimestamp}`)
    })

    it('debe acceder al dashboard correctamente', () => {
      cy.visit('/dashboard')
      cy.get('body').should('exist')
    })
  })
})
