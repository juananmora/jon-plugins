# Ejemplos de Tests por Tipo de Componente

## Estructura de test (patrón AAA)

Todos los tests deben seguir el patrón **Arrange-Act-Assert** con `@DisplayName` en formato Given-When-Then.

```java
@ExtendWith(MockitoExtension.class)
class ResourceServiceTest {
    
    @Mock
    private ResourceRepository repository;
    
    @Mock
    private ResourceMapper mapper;
    
    @InjectMocks
    private ResourceServiceImpl service;
    
    private Resource testResource;
    private ResourceDTO testDto;
    
    @BeforeEach
    void setUp() {
        testResource = createTestResource();
        testDto = createTestDto();
    }
    
    @Test
    @DisplayName("Given valid id, When findById, Then return resource")
    void testFindById_WithValidId_ShouldReturnResource() {
        // Arrange
        String id = "RES-001";
        when(repository.findById(id)).thenReturn(Optional.of(testResource));
        when(mapper.toDto(testResource)).thenReturn(testDto);
        
        // Act
        ResourceDTO result = service.findById(id);
        
        // Assert
        assertNotNull(result);
        assertEquals(testDto.getId(), result.getId());
        
        verify(repository).findById(id);
        verify(mapper).toDto(testResource);
    }
    
    @Test
    @DisplayName("Given invalid id, When findById, Then throw NotFoundException")
    void testFindById_WithInvalidId_ShouldThrowNotFoundException() {
        // Arrange
        String id = "INVALID";
        when(repository.findById(id)).thenReturn(Optional.empty());
        
        // Act & Assert
        assertThrows(ResourceNotFoundException.class, 
            () -> service.findById(id));
        
        verify(repository).findById(id);
        verifyNoInteractions(mapper);
    }
}
```

## Controller Tests (MockMvc / @WebMvcTest)

```java
@WebMvcTest(ResourceController.class)
class ResourceControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private ResourceService service;
    
    @Test
    void testGetById_ShouldReturn200() throws Exception {
        when(service.findById("1")).thenReturn(testDto);
        
        mockMvc.perform(get("/api/v1/resource/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value("1"));
    }
}
```

## Repository Tests (DataJpaTest)

```java
@DataJpaTest
class ResourceRepositoryTest {
    
    @Autowired
    private ResourceRepository repository;
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Test
    void testFindByStatus_ShouldReturnFiltered() {
        entityManager.persist(createResource("ACTIVE"));
        entityManager.flush();
        
        List<Resource> result = repository.findByStatus("ACTIVE");
        
        assertEquals(1, result.size());
    }
}
```
