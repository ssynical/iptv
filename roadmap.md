# iptv backend roadmap

## core foundation
- [x] project structure setup
- [x] database models and schemas
- [x] basic authentication system
- [x] core api endpoints structure

## authentication & user management
- [x] user registration/login endpoints
- [x] token-based authentication
- [x] user permissions and roles
- [x] subscription management
  - [x] user subscription status
  - [x] expiry date handling
  - [ ] active connections tracking

## xtream codes api compatibility
- [x] player_api.php endpoints (basic)
  - [x] get_series_categories
  - [x] get_vod_categories  
  - [x] get_live_categories
  - [x] get_series
  - [x] get_vod_streams
  - [x] get_live_streams
  - [ ] get_series_info
  - [ ] get_vod_info
- [ ] xmltv epg support
- [ ] m3u playlist generation

## content management
- [x] stream/channel crud operations
- [x] category management system
- [ ] series/vod metadata handling
- [ ] epg data management

## streaming infrastructure
- [ ] stream url generation and validation
- [ ] load balancing for multiple servers
- [ ] connection limits enforcement
- [ ] stream health monitoring

## admin panel backend
- [x] user management endpoints (basic)
- [x] content management endpoints (basic)
- [ ] statistics and analytics
- [ ] system monitoring endpoints

## client applications support
- [ ] mobile app api endpoints
- [ ] web player integration
- [ ] third-party app compatibility testing

## production features
- [ ] logging and monitoring
- [ ] error handling and recovery
- [ ] rate limiting
- [ ] security hardening
- [ ] performance optimization
- [x] deployment configuration (docker)

## finishing touches
- [ ] api documentation
- [ ] unit tests
- [ ] integration tests
- [x] docker containerization
- [ ] ci/cd pipeline setup

## next immediate priorities
- [ ] m3u playlist generation
- [ ] stream url generation with authentication
- [ ] connection limits enforcement
- [ ] get_series_info and get_vod_info endpoints
- [ ] series episodes management
- [ ] xmltv epg basic support