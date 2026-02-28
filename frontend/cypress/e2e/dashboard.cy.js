// Test de Dashboard y Navegación - Campus Guardian
describe('Dashboard y Navegación', () => {
  let testData
  
  before(() => {
    cy.fixture('testData.json').then((data) => {
      testData = data
    })
  })
  
  beforeEach(() => {
    cy.login(testData.testUsers.ciudadano.email, testData.testUsers.ciudadano.password)
  })

  describe('Dashboard Principal - Ciudadano', () => {
    it('debe cargar el dashboard correctamente', () => {
      cy.visit('/dashboard')
      cy.url().should('include', '/dashboard')
      cy.get('body').should('exist')
    })

    it('debe abrir y cerrar el menú hamburguesa', () => {
      cy.visit('/dashboard')
      
      // Abrir menú
      cy.get('.hamburger-btn').click()
      cy.get('.mobile-menu', { timeout: 2000 }).should('be.visible')
      
      // Cerrar menú
      cy.get('.menu-close-btn').click()
      cy.get('.mobile-menu', { timeout: 2000 }).should('not.exist')
    })

    it('debe navegar a Mapa desde el menú', () => {
      cy.visit('/dashboard')
      cy.get('.hamburger-btn').click()
      cy.get('.menu-link[href="/mapa"]').click()
      cy.url({ timeout: 5000 }).should('include', '/mapa')
    })

    it('debe navegar a Incidencias desde el menú', () => {
      cy.visit('/dashboard')
      cy.get('.hamburger-btn').click()
      cy.get('.menu-link[href="/incidencias"]').click()
      cy.url({ timeout: 5000 }).should('include', '/incidencias')
    })

    it('debe navegar a Mis Incidencias desde el menú', () => {
      cy.visit('/dashboard')
      cy.get('.hamburger-btn').click()
      cy.get('.menu-link[href="/mis-incidencias"]').click()
      cy.url({ timeout: 5000 }).should('include', '/mis-incidencias')
    })

    it('debe mostrar información del usuario en el menú', () => {
      cy.visit('/dashboard')
      cy.get('.hamburger-btn').click()
      cy.get('.menu-header').should('be.visible')
      cy.get('.user-avatar, .avatar-initials').should('exist')
      cy.get('.role-badge').should('exist')
    })

    it('debe poder acceder al perfil desde el menú', () => {
      cy.visit('/dashboard')
      cy.get('.hamburger-btn').click()
      cy.contains('button', 'Editar Perfil').click()
      cy.url({ timeout: 5000 }).should('include', '/perfil')
    })
  })

  describe('Dashboard y Menú - Admin', () => {
    beforeEach(() => {
      cy.logout()
      cy.login(testData.testUsers.admin.email, testData.testUsers.admin.password)
    })

    it('debe redirigir a admin después del login', () => {
      // El admin ya inició sesión en beforeEach y fue redirigido a /admin
      cy.url().should('include', '/admin')
    })

    it('debe permitir a admin acceder al dashboard manualmente', () => {
      cy.visit('/dashboard')
      cy.url().should('include', '/dashboard')
      cy.get('body').should('exist')
    })

    it('debe mostrar el menú con opciones de admin en dashboard', () => {
      cy.visit('/dashboard')
      cy.get('.hamburger-btn').click()
      cy.get('.menu-link[href="/admin/usuarios"]').should('exist')
    })
  })
})
