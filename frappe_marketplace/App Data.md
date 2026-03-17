# Frappe Marketplace App Data

## App Name
`erpnext_nextcloud_sso`

## App Title
Nextcloud SSO for ERPNext

## Short Description
Nextcloud OAuth2 SSO integration for ERPNext social login

## Long Description

Seamlessly integrate Nextcloud OAuth2 authentication with your ERPNext instance using this lightweight SSO integration app.

### Features

- **One-Click Configuration**: Built-in Nextcloud provider with pre-configured OAuth2 settings
- **Automatic User Provisioning**: Users authenticate via Nextcloud and are automatically provisioned in ERPNext
- **Secure OAuth2 Implementation**: Industry-standard OAuth2 authorization code flow
- **Email Normalization**: Automatic email validation and normalization for consistent user data
- **User-Friendly Setup**: Simple configuration through ERPNext's Social Login Key interface
- **No External Dependencies**: Pure Python implementation with minimal dependencies

### Use Cases

- **Organizations Using Nextcloud**: Perfect for companies already using Nextcloud for file storage and collaboration
- **Unified Authentication**: Streamline user management across Nextcloud and ERPNext
- **Single Sign-On**: Enable users to access ERPNext using their existing Nextcloud credentials
- **Enhanced Security**: Centralize authentication and leverage Nextcloud's security features

### How It Works

1. Install the app on your ERPNext instance
2. Create a Social Login Key in ERPNext
3. Select "Nextcloud" as the provider (appears in the dropdown automatically)
4. Configure your Nextcloud instance URL and OAuth credentials
5. Users can now log in to ERPNext using their Nextcloud accounts

The app handles the complete OAuth2 flow, including authorization, token exchange, and user info retrieval from Nextcloud's OCS API.

### Technical Details

- Compatible with ERPNext v16 and Frappe v16
- Uses Nextcloud's OAuth2 API and OCS Cloud API
- Supports custom Nextcloud instance URLs
- Email-based user matching and provisioning
- Comprehensive error handling and validation

### Support

For bug reports, feature requests, or contributions, please visit our GitHub repository.

## Categories
- Authentication / Security
- Integration
- Productivity

## Pricing
Free (Open Source - MIT License)

## Links

- **Repository**: https://github.com/b-robotized/erpnext_nextcloud_sso
- **Documentation**: https://github.com/b-robotized/erpnext_nextcloud_sso/blob/main/README.md
- **Issues**: https://github.com/b-robotized/erpnext_nextcloud_sso/issues
- **License**: https://github.com/b-robotized/erpnext_nextcloud_sso/blob/main/LICENSE

## Publisher Information

- **Publisher Name**: b»robotized group
- **Contact**: Dr. Denis Stogl (dr.denis@b-robotized.com)

## Version Compatibility

- Frappe Framework: v16.x
- ERPNext: v16.x

## Logo

Logo file: `icon.png` (located in the same directory)
- Format: PNG
- Size: Square format (suitable for circular display)
- Based on Nextcloud cloud icon (blue)

## Screenshots Needed

Before submission, prepare the following screenshots:

1. **Screenshot 1: Social Login Key Configuration**
   - Show the Social Login Key form with "Nextcloud" selected as provider
   - Display auto-populated fields (authorize_url, access_token_url, api_endpoint)
   - Highlight the ease of configuration

2. **Screenshot 2: Login Page**
   - Show ERPNext login page with Nextcloud login button visible
   - Demonstrate the user-facing login experience

3. **Screenshot 3: Successful Authentication**
   - Show a user successfully logged in via Nextcloud SSO
   - Can display user profile or dashboard after login

## Installation Instructions

*(Frappe Cloud handles installation automatically, but for reference)*

```bash
# On bench:
bench get-app erpnext_nextcloud_sso https://github.com/b-robotized/erpnext_nextcloud_sso.git
bench --site your-site.com install-app erpnext_nextcloud_sso

# On Frappe Cloud:
# Simply click "Install" from the marketplace
```

## Configuration Steps

1. **In Nextcloud:**
   - Go to Settings → Security → OAuth 2.0 clients
   - Create a new OAuth2 application
   - Note the Client ID and Client Secret
   - Set Redirect URI to: `https://your-erpnext-site.com/api/method/erpnext_nextcloud_sso.oauth2_logins.login_via_nextcloud`

2. **In ERPNext:**
   - Go to Social Login Key list
   - Create new Social Login Key
   - Select "Nextcloud" as Social Login Provider
   - Enter your Nextcloud base URL
   - Enter Client ID and Client Secret from Nextcloud
   - Save

3. **Test:**
   - Log out of ERPNext
   - You should see "Login with Nextcloud" button
   - Click to authenticate via Nextcloud

## Keywords/Tags

nextcloud, sso, oauth2, authentication, social-login, single-sign-on, integration, security, cloud

## Changelog

### Version 1.0.0 (Initial Release)
- OAuth2 integration with Nextcloud
- Automatic user provisioning
- Built-in Nextcloud provider configuration
- Email normalization and validation
- Comprehensive error handling
- CI/CD workflows for testing and deployment
- Docker-based development and testing environment

## Notes for Frappe Team Review

- This app provides a specific integration for Nextcloud SSO, filling a gap in ERPNext's social login capabilities
- The app follows Frappe Framework best practices and coding standards
- All code is well-documented and includes comprehensive unit tests
- The app has been tested with ERPNext v16 in Docker environments
- CI/CD is set up with GitHub Actions for automated testing
- The app is actively maintained and open to community contributions
