# Testing Strategies

Last Updated: 2025-01-06

## TDD London School Methodology

### Core Principles
1. **Outside-In Development**: Start from user-facing behavior
2. **Mock External Dependencies**: Isolate units under test
3. **Write Test First**: Define behavior before implementation
4. **One Test, One Behavior**: Keep tests focused
5. **Refactor with Confidence**: Only when tests are green

### TDD Cycle
```
1. RED: Write a failing test
   - Define expected behavior
   - Run test to see it fail
   - Ensure failure is for right reason

2. GREEN: Write minimal code to pass
   - Implement just enough
   - Don't over-engineer
   - Focus on making test pass

3. REFACTOR: Improve code quality
   - Maintain all green tests
   - Improve design
   - Remove duplication
```

## Test Organization Structure

### File Structure
```
src/
├── components/
│   ├── UserList.tsx
│   └── __tests__/
│       └── UserList.test.tsx
├── services/
│   ├── UserService.ts
│   └── __tests__/
│       └── UserService.test.ts
└── utils/
    ├── validators.ts
    └── __tests__/
        └── validators.test.ts
```

### Test Naming Conventions
```typescript
describe('ComponentName', () => {
  describe('methodName', () => {
    it('should return expected value when valid input provided', () => {});
    it('should throw error when input is invalid', () => {});
    it('should handle edge case gracefully', () => {});
  });
});
```

## Testing Patterns by Type

### Unit Testing

#### Component Testing (React/Frontend)
```typescript
describe('UserList', () => {
  it('should render user items when users provided', () => {
    // Arrange
    const users = [
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' }
    ];
    
    // Act
    const { getByText } = render(<UserList users={users} />);
    
    // Assert
    expect(getByText('John')).toBeInTheDocument();
    expect(getByText('Jane')).toBeInTheDocument();
  });
});
```

#### Service Testing (Backend)
```typescript
describe('UserService', () => {
  let mockRepository: jest.Mocked<UserRepository>;
  let service: UserService;
  
  beforeEach(() => {
    mockRepository = createMock<UserRepository>();
    service = new UserService(mockRepository);
  });
  
  describe('getUser', () => {
    it('should return user when found', async () => {
      // Arrange
      const expectedUser = { id: 1, name: 'John' };
      mockRepository.findById.mockResolvedValue(expectedUser);
      
      // Act
      const user = await service.getUser(1);
      
      // Assert
      expect(user).toEqual(expectedUser);
      expect(mockRepository.findById).toHaveBeenCalledWith(1);
    });
  });
});
```

### Integration Testing

#### API Testing
```typescript
describe('POST /api/users', () => {
  it('should create user when valid data provided', async () => {
    // Arrange
    const userData = { name: 'John', email: 'john@example.com' };
    
    // Act
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);
    
    // Assert
    expect(response.body).toMatchObject({
      id: expect.any(Number),
      ...userData
    });
  });
});
```

#### Database Testing
```typescript
describe('UserRepository', () => {
  let repository: UserRepository;
  
  beforeEach(async () => {
    await clearDatabase();
    repository = new UserRepository();
  });
  
  it('should persist and retrieve user', async () => {
    // Arrange
    const userData = { name: 'John', email: 'john@example.com' };
    
    // Act
    const created = await repository.create(userData);
    const retrieved = await repository.findById(created.id);
    
    // Assert
    expect(retrieved).toEqual(created);
  });
});
```

### End-to-End Testing

#### UI Flow Testing
```typescript
describe('User Registration Flow', () => {
  it('should complete registration process', async () => {
    // Navigate to registration
    await page.goto('/register');
    
    // Fill form
    await page.fill('[name="username"]', 'newuser');
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'securePass123');
    
    // Submit
    await page.click('button[type="submit"]');
    
    // Verify redirect and success message
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('.success-message')).toHaveText('Registration successful');
  });
});
```

## Mocking Strategies

### Types of Test Doubles
1. **Stub**: Returns predetermined values
2. **Mock**: Verifies interactions
3. **Spy**: Records calls for later verification
4. **Fake**: Simplified working implementation
5. **Dummy**: Placeholder with no behavior

### Mocking Best Practices
```typescript
// Mock external dependencies
jest.mock('../services/EmailService');

// Mock modules
jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn()
}));

// Mock timers
jest.useFakeTimers();

// Mock system functions
global.Date.now = jest.fn(() => 1234567890);
```

## Coverage Strategies

### Coverage Targets
- **Line Coverage**: 100% (default)
- **Branch Coverage**: 100% (all conditionals)
- **Function Coverage**: 100% (all functions called)
- **Statement Coverage**: 100% (all statements executed)

### Achieving High Coverage
1. **Test Happy Path**: Normal expected behavior
2. **Test Error Cases**: Invalid inputs, failures
3. **Test Edge Cases**: Boundary conditions
4. **Test All Branches**: Every if/else path
5. **Test Async Flows**: Promises, callbacks

### Coverage Exceptions
Document why coverage is skipped:
```typescript
/* istanbul ignore next - Platform specific code */
if (process.platform === 'win32') {
  // Windows-specific implementation
}
```

## Test Data Management

### Test Data Patterns
```typescript
// Factory pattern
const createUser = (overrides = {}) => ({
  id: 1,
  name: 'Default User',
  email: 'user@example.com',
  ...overrides
});

// Builder pattern
class UserBuilder {
  private user = { id: 1, name: '', email: '' };
  
  withName(name: string) {
    this.user.name = name;
    return this;
  }
  
  build() {
    return this.user;
  }
}
```

### Test Fixtures
```typescript
// fixtures/users.ts
export const validUser = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com'
};

export const invalidUser = {
  id: 'invalid',
  name: '',
  email: 'not-an-email'
};
```

## Performance Testing

### Load Testing
```typescript
describe('Performance', () => {
  it('should handle 1000 concurrent requests', async () => {
    const promises = Array(1000).fill(null).map(() => 
      request(app).get('/api/users')
    );
    
    const start = Date.now();
    const responses = await Promise.all(promises);
    const duration = Date.now() - start;
    
    expect(duration).toBeLessThan(5000); // 5 seconds
    expect(responses.every(r => r.status === 200)).toBe(true);
  });
});
```

### Benchmark Testing
```typescript
describe('Algorithm Performance', () => {
  it('should sort 10000 items in under 100ms', () => {
    const items = generateRandomArray(10000);
    
    const start = performance.now();
    const sorted = quickSort(items);
    const duration = performance.now() - start;
    
    expect(duration).toBeLessThan(100);
    expect(isSorted(sorted)).toBe(true);
  });
});
```

## Testing Anti-Patterns to Avoid

1. **Testing Implementation Details**: Focus on behavior
2. **Excessive Mocking**: Only mock boundaries
3. **Shared State**: Each test should be independent
4. **Testing Framework Code**: Trust the framework
5. **Flaky Tests**: Make tests deterministic
6. **Large Test Methods**: Keep tests focused
7. **No Assertion**: Every test needs expectations

## Continuous Testing

### Git Hooks
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "npm test",
      "pre-push": "npm run test:coverage"
    }
  }
}
```

### CI Pipeline
```yaml
# .github/workflows/test.yml
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - run: npm install
    - run: npm test -- --coverage
    - run: npm run test:e2e
```

## Testing Checklist

### Before Implementation
- [ ] Write test describing expected behavior
- [ ] Ensure test fails for right reason
- [ ] Consider edge cases and error scenarios

### During Implementation
- [ ] Write minimal code to pass test
- [ ] Run tests frequently
- [ ] Keep test and implementation in sync

### After Implementation
- [ ] All tests passing
- [ ] Coverage targets met
- [ ] No console errors/warnings
- [ ] Tests run quickly
- [ ] Tests are maintainable