# iptv backend roadmap

## core foundation
- [x] project structure setup
- [x] database models and schemas
- [x] basic authentication system
- [ ] core api endpoints structure

## authentication & user management
- [x] user registration/login endpoints
- [x] token-based authentication
- [ ] user permissions and roles
- [ ] subscription management
  - user subscription status
  - expiry date handling
  - active connections tracking

## xtream codes api compatibility
- [ ] player_api.php endpoints
  - get_series_categories
  - get_vod_categories  
  - get_live_categories
  - get_series
  - get_vod_streams
  - get_live_streams
  - get_series_info
  - get_vod_info
- [ ] xmltv epg support
- [ ] m3u playlist generation

## content management
- [ ] stream/channel crud operations
- [ ] category management system
- [ ] series/vod metadata handling
- [ ] epg data management

## streaming infrastructure
- [ ] stream url generation and validation
- [ ] load balancing for multiple servers
- [ ] connection limits enforcement
- [ ] stream health monitoring

## admin panel backend
- [ ] user management endpoints
- [ ] content management endpoints
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
- [ ] deployment configuration

## finishing touches
- [ ] api documentation
- [ ] unit tests
- [ ] integration tests
- [ ] docker containerization
- [ ] ci/cd pipeline setup