# Azure App Registration Certificate Monitor

## Overview

This Logic App monitors all Entra ID app registrations in your tenant and sends email alerts when certificates or secrets are expiring within 30 days.

**What it caught for us:** Azure Migrate appliances with expiring certificates that would have caused production migration failures.

## Features

- ✅ Monitors both certificates (keyCredentials) and secrets (passwordCredentials)
- ✅ Handles paginated Microsoft Graph API responses (100+ apps)
- ✅ 30-day expiration window (configurable)
- ✅ Extracts and includes app owners in email alerts
- ✅ HTML-formatted email report with statistics
- ✅ Daily execution at 6 AM (configurable)
- ✅ Secure credential storage via Azure Key Vault

## Prerequisites

### 1. Service Principal with Microsoft Graph API Permissions

Create an app registration in Entra ID with the following **Application** permissions:

- `Application.Read.All` - Read all app registrations
- `User.Read.All` - Read user details for owner expansion

**Important:** These must be **Application permissions**, not Delegated permissions.

Grant admin consent after adding the permissions.

### 2. Azure Key Vault

Store the following secrets in Azure Key Vault:

| Secret Name | Description |
|------------|-------------|
| `YOUR-TENANT-ID-SECRET` | Your Azure AD tenant ID (GUID) |
| `YOUR-CLIENT-ID-SECRET` | Service principal client/application ID |
| `YOUR-CLIENT-SECRET` | Service principal client secret value |

### 3. Logic App Connections

You'll need to configure two connections:

- **Key Vault connection** - For retrieving credentials
- **Office 365 connection** - For sending email alerts

## Deployment Instructions

### Step 1: Create the Logic App

1. Go to Azure Portal → Create Resource → Logic App
2. Choose **Consumption** plan
3. Select your resource group and region
4. Click **Review + Create**

### Step 2: Import the Definition

1. Open the Logic App
2. Go to **Logic app code view**
3. Replace the entire JSON with the contents of `certificate-monitor-logic-app.json`
4. Click **Save**

### Step 3: Configure Connections

1. Go back to **Logic app designer**
2. You'll see errors on actions that need connections
3. For each connection:
   - Click the action with the error
   - Select "Add new connection"
   - Authenticate with appropriate credentials
   - Save

### Step 4: Update Key Vault Secret Names

If your Key Vault secret names differ from the defaults:

1. Open the **Tenant_ID**, **Client_ID**, and **Client_Secret** actions
2. Update the `secretName` parameter to match your secret names

### Step 5: Update Email Recipients

1. Open the **Send_Email** action
2. Update the `To` and `From` fields with your team's email addresses
3. Save the Logic App

### Step 6: Test the Workflow

1. Click **Run Trigger** → **Recurrence**
2. Wait 1-2 minutes for execution to complete
3. Check your email for the report

## Customization Options

### Change Expiration Window

The default is 30 days. To modify:

1. Find the condition: `@ticks(addDays(utcNow(), 30))`
2. Change `30` to your desired number of days
3. This appears in two places (password expiry and certificate expiry checks)

### Change Execution Schedule

The default is daily at 6 AM Eastern. To modify:

1. Open the **Recurrence** trigger
2. Adjust the `schedule` parameters:
   - `hours`: Hour of day (0-23)
   - `minutes`: Minute of hour (0-59)
   - `timeZone`: Any valid Windows timezone

### Add Additional Email Recipients

The Logic App automatically includes app owners in email notifications.

To add static recipients:

1. Open the **Send_Email** action
2. Update the `To` field to include semicolon-separated email addresses

## Email Report Format

The email includes:

- **Statistics summary**: Total apps processed, apps with credentials, expiring credentials
- **Detailed table**: App name, App ID, credential type, expiration date, owner name, owner email
- **HTML formatting**: Styled table with proper spacing and borders

## Troubleshooting

### "Unauthorized" errors during Graph API calls

- Verify service principal has correct Graph API permissions
- Ensure admin consent was granted
- Check that credentials in Key Vault are correct

### No apps showing in report

- Verify the app registration has `Application.Read.All` permission
- Check that the credential expiration dates are within the configured window
- Run the Logic App manually and check the execution history

### Email not sending

- Verify the Office 365 connection is properly authenticated
- Check that the sender email address is valid
- Ensure recipients are valid email addresses

### Pagination not working (only seeing 100 apps)

- Check the **Until** loop condition
- Verify the `@odata.nextLink` parsing logic
- Review execution history to see if loop is terminating early

## What This Caught for Us

This Logic App was built for general certificate compliance monitoring, but it accidentally discovered a critical operational issue:

**Azure Migrate appliances have an 18-month expiration timer** that Microsoft doesn't warn you about. Our security compliance tool caught the expiring certificates 28 days before they would have killed our migration project.

Read the full story: [Azure Migrate's 18-Month Data Deletion](https://azure-noob.com/blog/azure-migrate-certificate-18-month-limit/)

## Technical Details

### Graph API Query

```
GET https://graph.microsoft.com/v1.0/applications
  ?$select=displayName,appId,passwordCredentials,keyCredentials
  &$expand=owners($select=displayName,userPrincipalName,mail)
  &$top=100
```

### Pagination Handling

The Logic App uses an `Until` loop with:
- Maximum 60 iterations
- 1-hour timeout
- Checks for `@odata.nextLink` in each response
- Merges results into a single array

### Authentication Flow

1. Retrieve credentials from Key Vault
2. Request OAuth token from Microsoft identity platform
3. Use bearer token for all Graph API calls
4. Token cached for workflow execution

## Security Considerations

- ✅ Credentials stored in Azure Key Vault (not in Logic App definition)
- ✅ Service principal uses least-privilege permissions
- ✅ Secure data enabled for credential actions
- ✅ No secrets logged in execution history
- ✅ Owner email addresses only exposed to authorized recipients

## Cost Estimate

**Logic App Execution:**
- Consumption plan: ~$0.000125 per action execution
- Daily run with 500 apps: ~250 actions
- Monthly cost: ~$1.00

**Key Vault:**
- Secret operations: $0.03 per 10,000 operations
- Daily run = 3 secrets × 30 days = negligible cost

**Total estimated cost: $1-2/month**

## Support

For questions or issues:
- Check [Azure Migrate Certificate Post](https://azure-noob.com/blog/azure-migrate-certificate-18-month-limit/) for context
- Review Logic App execution history for detailed error messages
- Verify Microsoft Graph API permissions and consent

## License

This Logic App definition is provided as-is for educational and operational use.

No warranty or support is provided.
