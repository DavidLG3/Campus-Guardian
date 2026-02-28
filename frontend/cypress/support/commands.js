// ***********************************************
// Custom Commands for Campus Guardian Tests
// ***********************************************

/**
 * Login command - Makes authentication easier in tests
 * @param {string} email - User email
 * @param {string} password - User password
 * 
 * @example
 * cy.login('test_admin@campusguardian.test', 'Admin123!')
 */
Cypress.Commands.add('login', (email, password) => {
  // Configurar interceptor ANTES de visitar la página
  cy.intercept('POST', '**/api/auth/login/').as('loginRequest')
  
  cy.visit('/login')
  
  // El formulario usa id="email" y id="password"
  cy.get('#email').should('be.visible').clear().type(email)
  cy.get('#password').should('be.visible').clear().type(password)
  
  cy.get('button[type="submit"]').click()
  
  // Esperar a que la petición de login complete
  cy.wait('@loginRequest')
  
  // Esperar a que se complete la redirección (la URL ya no debe contener /login)
  cy.url({ timeout: 15000 }).should('match', /\/(dashboard|home|admin)/)
})

/**
 * Login command via API - Faster for tests that don't need to test the login UI
 * @param {string} email - User email
 * @param {string} password - User password
 */
Cypress.Commands.add('loginAPI', (email, password) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/auth/login/',
    body: {
      email,
      password
    },
    failOnStatusCode: false
  }).then((response) => {
    if (response.status === 200) {
      window.localStorage.setItem('token', response.body.token)
      window.localStorage.setItem('user', JSON.stringify(response.body.user))
    }
  })
})

/**
 * Logout command - Logs out the current user
 */
Cypress.Commands.add('logout', () => {
  // Verificar si existe el botón hamburguesa
  cy.get('body').then($body => {
    if ($body.find('.hamburger-btn').length > 0) {
      // Si existe el menú, hacer logout normal
      cy.get('.hamburger-btn').click()
      cy.wait(500)
      cy.contains(/cerrar sesión|logout|salir/i).click()
      cy.url({ timeout: 5000 }).should('eq', 'http://localhost:5173/')
    } else {
      // Si no existe, limpiar localStorage manualmente
      cy.clearLocalStorage()
      cy.visit('/login')
    }
  })
})

/**
 * Cleanup test data - Removes test data created during tests
 * This includes users with TEST in their names and incidencias with TEST in title
 */
Cypress.Commands.add('cleanupTestData', () => {
  // Login as admin to perform cleanup
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/auth/login/',
    body: {
      username: 'admin',
      password: 'admin123'
    },
    failOnStatusCode: false
  }).then((authResponse) => {
    if (authResponse.status === 200) {
      const token = authResponse.body.token
      
      // Clean up test incidencias (those with TEST in title)
      cy.request({
        method: 'GET',
        url: 'http://localhost:8000/api/incidencias/',
        headers: {
          'Authorization': `Token ${token}`
        },
        failOnStatusCode: false
      }).then((response) => {
        if (response.status === 200 && response.body.results) {
          const testIncidencias = response.body.results.filter(inc => 
            inc.titulo && inc.titulo.includes('TEST')
          )
          
          testIncidencias.forEach(inc => {
            cy.request({
              method: 'DELETE',
              url: `http://localhost:8000/api/incidencias/${inc.id}/`,
              headers: {
                'Authorization': `Token ${token}`
              },
              failOnStatusCode: false
            })
          })
        }
      })
      
      // Clean up test users (those with test_ in username)
      cy.request({
        method: 'GET',
        url: 'http://localhost:8000/api/usuarios/',
        headers: {
          'Authorization': `Token ${token}`
        },
        failOnStatusCode: false
      }).then((response) => {
        if (response.status === 200) {
          const users = Array.isArray(response.body) ? response.body : response.body.results || []
          const testUsers = users.filter(user => 
            user.username && (user.username.includes('test_') || user.username.includes('seguridad_test'))
          )
          
          testUsers.forEach(user => {
            cy.request({
              method: 'DELETE',
              url: `http://localhost:8000/api/usuarios/${user.id}/`,
              headers: {
                'Authorization': `Token ${token}`
              },
              failOnStatusCode: false
            })
          })
        }
      })
    }
  })
})

/**
 * Create a test incidencia - Clicks on map and fills form
 * @param {object} data - Incidencia data
 */
Cypress.Commands.add('createIncidencia', (data = {}) => {
  const timestamp = Date.now()
  const incidencia = {
    tipo: data.tipo || 'otro',
    descripcion: data.descripcion || 'Descripción de prueba',
    direccion: data.direccion || '',
    latitud: data.latitud || 40.5472,
    longitud: data.longitud || -3.6878,
    ...data
  }
  
  cy.visit('/incidencias/nueva')
  
  // Seleccionar tipo
  cy.get('#tipo').select(incidencia.tipo)
  
  // Llenar descripción
  cy.get('#descripcion').type(incidencia.descripcion)
  
  // Click en el mapa para establecer ubicación
  cy.wait(1000) // Esperar a que cargue el mapa
  cy.get('#incidencia-map').click()
  
  // Si se proporciona dirección
  if (incidencia.direccion) {
    cy.get('#direccion').type(incidencia.direccion)
  }
  
  // Enviar formulario
  cy.get('button[type="submit"]').click()
  
  return cy.wrap(incidencia)
})

/**
 * Navigate using keyboard (Tab)
 */
Cypress.Commands.add('tab', { prevSubject: 'optional' }, (subject) => {
  cy.wrap(subject).trigger('keydown', { keyCode: 9, which: 9 })
  return subject ? cy.wrap(subject) : cy.focused()
})
