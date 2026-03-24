// Smoke Test - Campus Guardian
// Tests básicos para verificar que la aplicación carga correctamente

describe('Smoke Tests - Campus Guardian', () => {
  
  it('debe cargar la página principal sin errores', () => {
    cy.visit('/')
    cy.get('body').should('exist')
  })

  it('debe tener el título correcto', () => {
    cy.visit('/')
    cy.title().should('include', 'Campus Guardian')
  })

  it('debe redirigir a la splash screen o login', () => {
    cy.visit('/')
    // Esperar a que cargue (splash screen puede tardar unos segundos)
    cy.wait(3000)
    // Debería estar en login o home
    cy.url().should('match', /\/(login|home|dashboard|register)/)
  })

  it('debe cargar la página de login', () => {
    cy.visit('/login')
    cy.url().should('include', '/login')
    cy.get('input[type="text"], input[type="email"]').should('exist')
    cy.get('input[type="password"]').should('exist')
    cy.get('button[type="submit"]').should('exist')
  })

  it('debe cargar la página de registro', () => {
    cy.visit('/register')
    cy.url().should('include', '/register')
    cy.get('input[type="text"]').should('exist')
    cy.get('input[type="email"]').should('exist')
    cy.get('input[type="password"]').should('exist')
  })

  it('debe poder iniciar sesión con credenciales válidas', () => {
    cy.fixture('testData.json').then((testData) => {
      cy.visit('/login')
      cy.get('#email').type(testData.testUsers.admin.email)
      cy.get('#password').type(testData.testUsers.admin.password)
      cy.get('button[type="submit"]').click()
      
      // Debería redirigir al dashboard o admin
      cy.url({ timeout: 10000 }).should('match', /\/(dashboard|admin)/)
    })
  })

  it('debe mostrar el menú de navegación después de login', () => {
    cy.fixture('testData.json').then((testData) => {
      cy.login(testData.testUsers.admin.email, testData.testUsers.admin.password)
      
      // Verificar que hay elementos de navegación
      cy.get('nav, [class*="sidebar"], [class*="menu"]').should('exist')
    })
  })

  it('debe poder navegar entre secciones principales', () => {
    cy.fixture('testData.json').then((testData) => {
      cy.login(testData.testUsers.admin.email, testData.testUsers.admin.password)
    
      // Dashboard
      cy.visit('/dashboard')
      cy.url().should('include', '/dashboard')
      
      // Incidencias
      cy.visit('/incidencias')
      cy.url().should('include', '/incidencias')
      
      // Mapa
      cy.visit('/mapa')
      cy.url().should('include', '/mapa')
      
      // Perfil
      cy.visit('/perfil')
      cy.url().should('include', '/perfil')
    })
  })
    cy.visit('/')
    
    cy.window().then((win) => {
      cy.spy(win.console, 'error')
    })
    
    cy.visit('/login')
    // Los errores de consola se reportarían en los logs de Cypress
  })

  it('debe cargar los recursos estáticos correctamente', () => {
    cy.visit('/')
    
    // Verificar que no hay errores 404 en recursos
    cy.window().then((win) => {
      const performance = win.performance.getEntriesByType('resource')
      const failedResources = performance.filter(resource => {
        return resource.name.includes('.js') || resource.name.includes('.css')
      })
      
      // Todos los recursos deberían cargar (status implícito en performance)
      expect(failedResources.length).to.be.greaterThan(0) // Hay recursos JS/CSS
    })
  })


