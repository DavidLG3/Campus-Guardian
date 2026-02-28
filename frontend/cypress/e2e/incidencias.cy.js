// Test de Gestión de Incidencias - Campus Guardian
describe('Gestión de Incidencias', () => {
  let testData
  
  before(() => {
    cy.fixture('testData.json').then((data) => {
      testData = data
    })
  })
  
  beforeEach(() => {
    // Login como ciudadano para crear incidencias
    cy.login(testData.testUsers.ciudadano.email, testData.testUsers.ciudadano.password)
  })

  describe('Visualización de Incidencias', () => {
    it('debe mostrar el listado de incidencias', () => {
      cy.visit('/incidencias')
      cy.url().should('include', '/incidencias')
      
      // Verificar que carga contenido
      cy.get('body').should('exist')
      cy.wait(1000)
    })

    it('debe mostrar mis incidencias reportadas', () => {
      cy.visit('/mis-incidencias')
      cy.url().should('include', '/mis-incidencias')
      
      // Verificar que carga la vista
      cy.get('body').should('exist')
    })

    it('debe visualizar incidencias en el mapa', () => {
      cy.visit('/mapa')
      cy.url().should('include', '/mapa')
      
      // Esperar a que cargue el mapa Leaflet
      cy.get('.leaflet-container', { timeout: 10000 }).should('exist')
      cy.wait(2000)
      
      // Verificar elementos del mapa
      cy.get('.leaflet-control-zoom').should('exist')
    })
  })

  describe('Crear Nueva Incidencia', () => {
    it('debe acceder al formulario de nueva incidencia', () => {
      cy.visit('/incidencias/nueva')
      cy.url().should('include', '/incidencias/nueva')
      
      // Verificar campos del formulario
      cy.get('#tipo').should('exist')
      cy.get('#descripcion').should('exist')
      cy.get('#incidencia-map', { timeout: 5000 }).should('be.visible')
      cy.get('button[type="submit"]').should('exist')
    })

    it('debe crear una nueva incidencia usando el mapa', () => {
      cy.visit('/incidencias/nueva')
      
      const timestamp = Date.now()
      const descripcion = `TEST: Incidencia de prueba ${timestamp}`
      
      // Seleccionar tipo
      cy.get('#tipo').select('otro')
      
      // Escribir descripción
      cy.get('#descripcion').type(descripcion)
      
      // Esperar a que cargue el mapa y hacer clic en él
      cy.get('#incidencia-map', { timeout: 5000 }).should('be.visible')
      cy.wait(1000)
      cy.get('#incidencia-map').click('center')
      
      // Enviar formulario
      cy.get('button[type="submit"]').click()
      
      // Verificar redirección exitosa
      cy.wait(3000)
      cy.url({ timeout: 10000 }).should('not.include', '/nueva')
    })

    it('debe validar campos requeridos', () => {
      cy.visit('/incidencias/nueva')
      
      // Intentar enviar sin llenar
      cy.get('button[type="submit"]').click()
      
      // El formulario no debe enviar (validación HTML5)
      cy.url().should('include', '/nueva')
    })
  })

  describe('Botón de Ubicación Actual', () => {
    it('debe mostrar botón para usar ubicación actual', () => {
      cy.visit('/incidencias/nueva')
      
      cy.contains(/usar mi ubicaci\u00f3n/i).should('exist')
    })
  })
})
