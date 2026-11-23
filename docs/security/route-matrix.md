# Route matrix

Generated from the FastAPI application with all installable apps enabled (`INSTALLED_APPS=hrms,crm,project_management`) using `app.routes`.

| Column | Meaning |
| --- | --- |
| Auth dependency | Authentication dependency detected on the route (`NONE` = no auth). |
| Permission required | Permissions or roles required by the dependency; `superuser` for admin-only routes. |
| Risk | Flagged when a route with no auth or only `get_current_user` touches payroll, employee PII, documents, or AI cost/usage data. |
| Review outcome | `handler-scoped` means the endpoint source contains an explicit ownership/permission check; `REVIEW` needs manual confirmation. This is a heuristic, not a proof. |

96 of 870 routes are flagged at dependency level; 0 still need manual review after source inspection.

| Method | Path | Auth dependency | Permission required | Risk | Review outcome | Tags | Summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GET | `/` | public | - | - | - | - | root |
| GET | `/api/v1/ai-agents` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | list_agents |
| GET | `/api/v1/ai-agents/analytics/by-agent` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | analytics_by_agent |
| GET | `/api/v1/ai-agents/analytics/by-module` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | analytics_by_module |
| GET | `/api/v1/ai-agents/analytics/by-user` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | analytics_by_user |
| GET | `/api/v1/ai-agents/analytics/cost` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | analytics_cost |
| GET | `/api/v1/ai-agents/analytics/summary` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | analytics_summary |
| GET | `/api/v1/ai-agents/approvals/pending` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | pending_approvals |
| POST | `/api/v1/ai-agents/approvals/{approval_id}/approve` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | approve_ai_action |
| POST | `/api/v1/ai-agents/approvals/{approval_id}/reject` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | reject_ai_action |
| GET | `/api/v1/ai-agents/config` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | ai_config |
| PUT | `/api/v1/ai-agents/config/{agent_id}` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | update_ai_config |
| GET | `/api/v1/ai-agents/conversations` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | list_conversations |
| POST | `/api/v1/ai-agents/conversations` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | create_conversation |
| GET | `/api/v1/ai-agents/conversations/{conversation_id}` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | get_conversation |
| GET | `/api/v1/ai-agents/conversations/{conversation_id}/export` | get_current_user | - | MEDIUM - user-only (documents, AI cost/usage) | handler-scoped (_require_) | AI Agents | export_conversation |
| GET | `/api/v1/ai-agents/conversations/{conversation_id}/messages` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | get_conversation_messages |
| POST | `/api/v1/ai-agents/conversations/{conversation_id}/messages` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | save_conversation_message |
| GET | `/api/v1/ai-agents/cost/by-agent` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | cost_by_agent |
| GET | `/api/v1/ai-agents/cost/by-user` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | cost_by_user |
| GET | `/api/v1/ai-agents/cost/summary` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | analytics_cost |
| GET | `/api/v1/ai-agents/feedback` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | list_feedback |
| GET | `/api/v1/ai-agents/handoff-notes` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | list_handoff |
| POST | `/api/v1/ai-agents/handoff-notes` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | create_handoff |
| PATCH | `/api/v1/ai-agents/handoff-notes/{note_id}/status` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | update_handoff_status |
| GET | `/api/v1/ai-agents/logs` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | ai_logs |
| POST | `/api/v1/ai-agents/messages/{message_id}/feedback` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | create_feedback |
| GET | `/api/v1/ai-agents/security/events` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | security_events |
| GET | `/api/v1/ai-agents/security/permissions` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | get_permissions |
| PUT | `/api/v1/ai-agents/security/permissions` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | update_permissions |
| GET | `/api/v1/ai-agents/security/settings` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | get_security_settings |
| PUT | `/api/v1/ai-agents/security/settings` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | update_security_settings |
| GET | `/api/v1/ai-agents/security/summary` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_, current_user.id) | AI Agents | security_summary |
| POST | `/api/v1/ai-agents/tools/test` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | test_ai_tool |
| GET | `/api/v1/ai-agents/usage/limits` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | get_usage_limits |
| PUT | `/api/v1/ai-agents/usage/limits` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | update_usage_limits |
| GET | `/api/v1/ai-agents/usage/summary` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | usage_summary |
| GET | `/api/v1/ai-agents/{agent_id}` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | get_agent |
| POST | `/api/v1/ai-agents/{agent_id}/chat` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | chat_with_agent |
| PATCH | `/api/v1/ai-agents/{agent_id}/status` | get_current_user | - | MEDIUM - user-only (AI cost/usage) | handler-scoped (_require_) | AI Agents | update_agent_status |
| POST | `/api/v1/ai/assistant` | RequirePermission, get_current_user | ai_assistant | - | - | AI Services | chat_with_assistant |
| GET | `/api/v1/ai/attrition-risk` | RequirePermission, get_current_user | reports_view | - | - | AI Services | attrition_risk |
| GET | `/api/v1/ai/attrition-risk/{employee_id}` | RequirePermission, get_current_user | reports_view | - | - | AI Services | employee_attrition_risk |
| POST | `/api/v1/ai/helpdesk-reply/{ticket_id}` | RequirePermission, get_current_user | helpdesk_manage | - | - | AI Services | generate_helpdesk_reply |
| POST | `/api/v1/ai/parse-resume/{candidate_id}` | RequirePermission, get_current_user | recruitment_manage | - | - | AI Services | parse_resume |
| POST | `/api/v1/ai/payroll-anomaly/{payroll_run_id}` | RequirePermission, get_current_user | payroll_approve | - | - | AI Services | detect_payroll_anomalies |
| POST | `/api/v1/ai/policy-qa` | RequirePermission, get_current_user | ai_assistant | - | - | AI Services | policy_qa |
| GET | `/api/v1/assets/` | RequirePermission, get_current_user | asset_view | - | - | Asset Management | list_assets |
| POST | `/api/v1/assets/` | RequirePermission, get_current_user | asset_manage | - | - | Asset Management | create_asset |
| POST | `/api/v1/assets/assignments` | RequirePermission, get_current_user | asset_manage | - | - | Asset Management | assign_asset |
| PUT | `/api/v1/assets/assignments/{assignment_id}/return` | RequirePermission, get_current_user | asset_manage | - | - | Asset Management | return_asset |
| GET | `/api/v1/assets/categories` | RequirePermission, get_current_user | asset_view | - | - | Asset Management | list_categories |
| POST | `/api/v1/assets/categories` | RequirePermission, get_current_user | asset_manage | - | - | Asset Management | create_category |
| PUT | `/api/v1/assets/{asset_id}` | RequirePermission, get_current_user | asset_manage | - | - | Asset Management | update_asset |
| GET | `/api/v1/attendance/biometric/devices` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | list_biometric_devices |
| POST | `/api/v1/attendance/biometric/devices` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | create_biometric_device |
| POST | `/api/v1/attendance/biometric/import` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | import_biometric_punches |
| POST | `/api/v1/attendance/check-in` | get_current_user | - | - | - | Attendance | check_in |
| POST | `/api/v1/attendance/check-out` | get_current_user | - | - | - | Attendance | check_out |
| POST | `/api/v1/attendance/compute/{employee_id}/{work_date}` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | compute_attendance_day |
| GET | `/api/v1/attendance/employee/{employee_id}` | RequirePermission, get_current_user | attendance_view | - | - | Attendance | employee_attendance |
| GET | `/api/v1/attendance/geo/policies` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | list_geo_policies |
| POST | `/api/v1/attendance/geo/policies` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | create_geo_policy |
| POST | `/api/v1/attendance/geo/punch` | get_current_user | - | - | - | Attendance | create_geo_punch |
| GET | `/api/v1/attendance/holidays` | get_current_user | - | - | - | Attendance | list_holidays |
| POST | `/api/v1/attendance/holidays` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | create_holiday |
| DELETE | `/api/v1/attendance/holidays/{holiday_id}` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | delete_holiday |
| PUT | `/api/v1/attendance/holidays/{holiday_id}` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | update_holiday |
| POST | `/api/v1/attendance/locks` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | lock_attendance_month |
| PUT | `/api/v1/attendance/locks/{lock_id}/unlock` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | unlock_attendance_month |
| GET | `/api/v1/attendance/my` | get_current_user | - | - | - | Attendance | my_attendance |
| GET | `/api/v1/attendance/punches` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | list_raw_punches |
| POST | `/api/v1/attendance/punches` | get_current_user | - | - | - | Attendance | create_raw_punch |
| POST | `/api/v1/attendance/regularize` | get_current_user | - | - | - | Attendance | request_regularization |
| GET | `/api/v1/attendance/regularize/pending` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | pending_regularizations |
| PUT | `/api/v1/attendance/regularize/{reg_id}/approve` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | approve_regularization |
| POST | `/api/v1/attendance/roster` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | assign_roster |
| GET | `/api/v1/attendance/shifts` | get_current_user | - | - | - | Attendance | list_shifts |
| POST | `/api/v1/attendance/shifts` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | create_shift |
| DELETE | `/api/v1/attendance/shifts/{shift_id}` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | delete_shift |
| PUT | `/api/v1/attendance/shifts/{shift_id}` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | update_shift |
| GET | `/api/v1/attendance/summary/monthly` | get_current_user | - | - | - | Attendance | monthly_summary |
| GET | `/api/v1/attendance/today` | get_current_user | - | - | - | Attendance | get_today_status |
| GET | `/api/v1/attendance/today-summary` | RequirePermission, get_current_user | attendance_view | - | - | Attendance | today_attendance_summary |
| GET | `/api/v1/attendance/weekly-offs` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | list_weekly_offs |
| POST | `/api/v1/attendance/weekly-offs` | RequirePermission, get_current_user | attendance_manage | - | - | Attendance | create_weekly_off |
| POST | `/api/v1/auth/change-password` | get_current_user | - | - | - | Authentication | change_password |
| POST | `/api/v1/auth/login` | public | - | - | - | Authentication | login |
| GET | `/api/v1/auth/login-attempts` | get_current_user | - | - | - | Authentication | list_login_attempts |
| POST | `/api/v1/auth/logout` | get_current_user | - | - | - | Authentication | logout |
| GET | `/api/v1/auth/me` | get_current_user | - | - | - | Authentication | get_me |
| POST | `/api/v1/auth/mfa-methods` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | create_mfa_method |
| PUT | `/api/v1/auth/mfa-methods/{method_id}/verify` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | verify_mfa_method |
| POST | `/api/v1/auth/mfa/confirm` | get_current_user | - | - | - | Authentication | Verify the setup code and enable TOTP MFA for the current user. |
| DELETE | `/api/v1/auth/mfa/disable` | get_current_user | - | - | - | Authentication | Disable TOTP MFA after verifying the current code. |
| POST | `/api/v1/auth/mfa/regenerate-recovery-codes` | get_current_user | - | - | - | Authentication | Regenerate one-time recovery codes after TOTP verification. |
| POST | `/api/v1/auth/mfa/setup` | get_current_user | - | - | - | Authentication | Start TOTP MFA setup and return one-time recovery codes. |
| GET | `/api/v1/auth/mfa/status` | get_current_user | - | - | - | Authentication | Return current MFA state for the logged-in user. |
| POST | `/api/v1/auth/mfa/verify` | public | - | - | - | Authentication | Complete the second login phase using TOTP or a recovery code. |
| GET | `/api/v1/auth/password-policies` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | list_password_policies |
| POST | `/api/v1/auth/password-policies` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | create_password_policy |
| PUT | `/api/v1/auth/password-policies/{policy_id}` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | Update password, lockout, and MFA policy settings. |
| POST | `/api/v1/auth/password-policies/{policy_id}/enforce-mfa` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | Enable MFA enforcement on a password policy and report remaining users. |
| GET | `/api/v1/auth/permissions` | get_current_user | - | - | - | Authentication | list_permissions |
| POST | `/api/v1/auth/refresh` | public | - | - | - | Authentication | refresh_token |
| GET | `/api/v1/auth/roles` | get_current_user | - | - | - | Authentication | list_roles |
| POST | `/api/v1/auth/roles` | get_current_user | - | - | - | Authentication | create_role |
| DELETE | `/api/v1/auth/roles/{role_id}` | get_current_user | - | - | - | Authentication | delete_role |
| PUT | `/api/v1/auth/roles/{role_id}` | get_current_user | - | - | - | Authentication | update_role |
| GET | `/api/v1/auth/sessions` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | list_user_sessions |
| POST | `/api/v1/auth/sessions` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | create_user_session |
| PUT | `/api/v1/auth/sessions/{session_id}/revoke` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | revoke_user_session |
| GET | `/api/v1/auth/sso/callback/oidc/{provider_id}` | NONE | - | - | - | SSO | Handle an OIDC callback, provision the user if allowed, and redirect to the frontend. |
| GET | `/api/v1/auth/sso/initiate/{provider_id}` | NONE | - | - | - | SSO | Start an OIDC SSO login by creating a stateful short-lived session. |
| GET | `/api/v1/auth/sso/providers` | get_current_active_superuser, get_current_user | superuser | - | - | SSO | List all SSO providers for administrators. |
| POST | `/api/v1/auth/sso/providers` | get_current_active_superuser, get_current_user | superuser | - | - | SSO | Create an SSO provider configuration. |
| GET | `/api/v1/auth/sso/providers/active` | NONE | - | - | - | SSO | Return active SSO providers safe for the login page. |
| DELETE | `/api/v1/auth/sso/providers/{provider_id}` | get_current_active_superuser, get_current_user | superuser | - | - | SSO | Soft-delete an SSO provider by disabling it. |
| PUT | `/api/v1/auth/sso/providers/{provider_id}` | get_current_active_superuser, get_current_user | superuser | - | - | SSO | Update an SSO provider; masked secrets are preserved. |
| GET | `/api/v1/auth/sso/providers/{provider_id}/sp-metadata` | get_current_active_superuser, get_current_user | superuser | - | - | SSO | Return minimal SAML SP metadata XML for a provider. |
| GET | `/api/v1/auth/sso/providers/{provider_id}/test` | get_current_active_superuser, get_current_user | superuser | - | - | SSO | Check whether configured OIDC endpoint URLs respond. |
| GET | `/api/v1/auth/users` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | list_users |
| POST | `/api/v1/auth/users` | get_current_active_superuser, get_current_user | superuser | - | - | Authentication | create_user |
| PUT | `/api/v1/background-verification/checks/{check_id}` | RequirePermission, get_current_user | recruitment_manage | - | - | Background Verification | update_check |
| GET | `/api/v1/background-verification/requests` | RequirePermission, get_current_user | recruitment_view | - | - | Background Verification | list_requests |
| POST | `/api/v1/background-verification/requests` | RequirePermission, get_current_user | recruitment_manage | - | - | Background Verification | create_request |
| PUT | `/api/v1/background-verification/requests/{request_id}` | RequirePermission, get_current_user | recruitment_manage | - | - | Background Verification | update_request |
| PUT | `/api/v1/background-verification/requests/{request_id}/consent` | RequirePermission, get_current_user | recruitment_manage | - | - | Background Verification | capture_consent |
| GET | `/api/v1/background-verification/requests/{request_id}/events` | RequirePermission, get_current_user | recruitment_view | - | - | Background Verification | list_connector_events |
| POST | `/api/v1/background-verification/requests/{request_id}/submit` | RequirePermission, get_current_user | recruitment_manage | - | - | Background Verification | submit_to_vendor |
| GET | `/api/v1/background-verification/vendors` | RequirePermission, get_current_user | recruitment_view | - | - | Background Verification | list_vendors |
| POST | `/api/v1/background-verification/vendors` | RequirePermission, get_current_user | recruitment_manage | - | - | Background Verification | create_vendor |
| POST | `/api/v1/background-verification/webhooks/{vendor_id}` | NONE | - | - | - | Background Verification | ingest_vendor_webhook |
| GET | `/api/v1/benefits/claims` | RequirePermission, get_current_user | payroll_view | - | - | Benefits Administration | list_claims |
| POST | `/api/v1/benefits/claims` | RequirePermission, get_current_user | payroll_view | - | - | Benefits Administration | create_claim |
| PUT | `/api/v1/benefits/claims/{claim_id}/review` | RequirePermission, get_current_user | payroll_approve | - | - | Benefits Administration | review_claim |
| GET | `/api/v1/benefits/enrollments` | RequirePermission, get_current_user | payroll_view | - | - | Benefits Administration | list_enrollments |
| POST | `/api/v1/benefits/enrollments` | RequirePermission, get_current_user | payroll_run | - | - | Benefits Administration | create_enrollment |
| GET | `/api/v1/benefits/esop/grants` | RequirePermission, get_current_user | payroll_view | - | - | Benefits Administration | list_esop_grants |
| POST | `/api/v1/benefits/esop/grants` | RequirePermission, get_current_user | payroll_run | - | - | Benefits Administration | create_esop_grant |
| GET | `/api/v1/benefits/esop/grants/{grant_id}/vesting` | RequirePermission, get_current_user | payroll_view | - | - | Benefits Administration | list_esop_vesting |
| GET | `/api/v1/benefits/esop/plans` | RequirePermission, get_current_user | payroll_view | - | - | Benefits Administration | list_esop_plans |
| POST | `/api/v1/benefits/esop/plans` | RequirePermission, get_current_user | payroll_run | - | - | Benefits Administration | create_esop_plan |
| POST | `/api/v1/benefits/flexi-allocations` | RequirePermission, get_current_user | payroll_run | - | - | Benefits Administration | create_flexi_allocation |
| GET | `/api/v1/benefits/flexi-policies` | RequirePermission, get_current_user | payroll_view | - | - | Benefits Administration | list_flexi_policies |
| POST | `/api/v1/benefits/flexi-policies` | RequirePermission, get_current_user | payroll_run | - | - | Benefits Administration | create_flexi_policy |
| POST | `/api/v1/benefits/payroll-deductions` | RequirePermission, get_current_user | payroll_run | - | - | Benefits Administration | create_payroll_deduction |
| GET | `/api/v1/benefits/plans` | RequirePermission, get_current_user | payroll_view | - | - | Benefits Administration | list_plans |
| POST | `/api/v1/benefits/plans` | RequirePermission, get_current_user | payroll_run | - | - | Benefits Administration | create_plan |
| GET | `/api/v1/company/` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_companies |
| POST | `/api/v1/company/` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_company |
| GET | `/api/v1/company/branches/` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_branches |
| POST | `/api/v1/company/branches/` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_branch |
| DELETE | `/api/v1/company/branches/{branch_id}` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | delete_branch |
| PUT | `/api/v1/company/branches/{branch_id}` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | update_branch |
| GET | `/api/v1/company/business-units` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_business_units |
| POST | `/api/v1/company/business-units` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_business_unit |
| GET | `/api/v1/company/cost-centers` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_cost_centers |
| POST | `/api/v1/company/cost-centers` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_cost_center |
| GET | `/api/v1/company/departments/` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_departments |
| POST | `/api/v1/company/departments/` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_department |
| DELETE | `/api/v1/company/departments/{dept_id}` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | delete_department |
| PUT | `/api/v1/company/departments/{dept_id}` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | update_department |
| GET | `/api/v1/company/designations/` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_designations |
| POST | `/api/v1/company/designations/` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_designation |
| DELETE | `/api/v1/company/designations/{desig_id}` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | delete_designation |
| PUT | `/api/v1/company/designations/{desig_id}` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | update_designation |
| GET | `/api/v1/company/grade-bands` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_grade_bands |
| POST | `/api/v1/company/grade-bands` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_grade_band |
| GET | `/api/v1/company/headcount-plans` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_headcount_plans |
| POST | `/api/v1/company/headcount-plans` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_headcount_plan |
| PUT | `/api/v1/company/headcount-plans/{plan_id}/approve` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | approve_headcount_plan |
| GET | `/api/v1/company/job-families` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_job_families |
| POST | `/api/v1/company/job-families` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_job_family |
| GET | `/api/v1/company/job-profiles` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_job_profiles |
| POST | `/api/v1/company/job-profiles` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_job_profile |
| GET | `/api/v1/company/locations` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_work_locations |
| POST | `/api/v1/company/locations` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_work_location |
| GET | `/api/v1/company/manager-hierarchy/validate` | RequirePermission, get_current_user | company_view | - | - | Company Setup | validate_manager_hierarchy |
| GET | `/api/v1/company/org-chart` | RequirePermission, get_current_user | company_view | - | - | Company Setup | org_chart |
| GET | `/api/v1/company/positions` | RequirePermission, get_current_user | company_view | - | - | Company Setup | list_positions |
| POST | `/api/v1/company/positions` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | create_position |
| DELETE | `/api/v1/company/{company_id}` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | delete_company |
| GET | `/api/v1/company/{company_id}` | RequirePermission, get_current_user | company_view | - | - | Company Setup | get_company |
| PUT | `/api/v1/company/{company_id}` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | update_company |
| POST | `/api/v1/company/{company_id}/logo` | RequirePermission, get_current_user | company_manage | - | - | Company Setup | upload_company_logo |
| GET | `/api/v1/crm/approval-workflows` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_approval_workflows |
| POST | `/api/v1/crm/approval-workflows` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | create_approval_workflow |
| PATCH | `/api/v1/crm/approval-workflows/{workflow_id}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | update_approval_workflow |
| GET | `/api/v1/crm/approvals` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_approvals |
| GET | `/api/v1/crm/approvals/my-pending` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | my_pending_approvals |
| POST | `/api/v1/crm/approvals/submit` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | submit_approval |
| POST | `/api/v1/crm/approvals/{request_id}/approve` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | approve_request |
| POST | `/api/v1/crm/approvals/{request_id}/reject` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | reject_request |
| GET | `/api/v1/crm/calendar` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | crm_calendar |
| GET | `/api/v1/crm/calendar-integrations` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_calendar_integrations |
| POST | `/api/v1/crm/calendar-integrations/connect` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | connect_calendar_integration |
| DELETE | `/api/v1/crm/calendar-integrations/{integration_id}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | delete_calendar_integration |
| POST | `/api/v1/crm/calendar/webhook` | NONE | - | - | - | CRM | Signed inbound calendar events. |
| POST | `/api/v1/crm/custom-field-values/upsert` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | upsert_custom_field_value |
| GET | `/api/v1/crm/custom-fields` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_custom_fields |
| GET | `/api/v1/crm/duplicates` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_duplicates |
| POST | `/api/v1/crm/duplicates/merge` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | merge_duplicates |
| POST | `/api/v1/crm/duplicates/scan` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | scan_duplicates |
| GET | `/api/v1/crm/email-templates` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_email_templates |
| POST | `/api/v1/crm/email-templates` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | create_email_template |
| POST | `/api/v1/crm/emails/send` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | send_crm_email |
| POST | `/api/v1/crm/enrichment/apply` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | enrichment_apply |
| GET | `/api/v1/crm/enrichment/history` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | enrichment_history |
| POST | `/api/v1/crm/enrichment/preview` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | enrichment_preview |
| GET | `/api/v1/crm/lead-scoring-rules` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_lead_scoring_rules |
| POST | `/api/v1/crm/leads/recalculate-scores` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | recalculate_lead_scores |
| POST | `/api/v1/crm/leads/{lead_id}/recalculate-score` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | recalculate_lead_score |
| POST | `/api/v1/crm/meetings/{meeting_id}/sync` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | sync_meeting_calendar |
| GET | `/api/v1/crm/message-templates` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_message_templates |
| POST | `/api/v1/crm/message-templates` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | create_message_template |
| GET | `/api/v1/crm/messages` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_crm_messages |
| POST | `/api/v1/crm/messages/send` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | send_crm_message |
| GET | `/api/v1/crm/module-info` | NONE | - | - | - | CRM | module_info |
| POST | `/api/v1/crm/pipelines/{pipeline_id}/stages` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | create_pipeline_stage |
| GET | `/api/v1/crm/quotations/{quotation_id}/pdf` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | generate_quotation_pdf |
| POST | `/api/v1/crm/quotations/{quotation_id}/send-pdf-email` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | send_quotation_pdf_email |
| GET | `/api/v1/crm/reports/revenue-trend` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view, reports_view | - | - | CRM | revenue_trend_report |
| GET | `/api/v1/crm/reports/sales-funnel` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view, reports_view | - | - | CRM | sales_funnel_report |
| GET | `/api/v1/crm/reports/territories` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view, reports_view | - | - | CRM | territory_report |
| GET | `/api/v1/crm/reports/win-loss` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view, reports_view | - | - | CRM | win_loss_report |
| GET | `/api/v1/crm/territories` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_territories |
| POST | `/api/v1/crm/territories` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | create_territory |
| POST | `/api/v1/crm/territories/auto-assign` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | auto_assign_territories |
| DELETE | `/api/v1/crm/territories/{territory_id}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | delete_territory |
| PATCH | `/api/v1/crm/territories/{territory_id}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | update_territory |
| POST | `/api/v1/crm/territories/{territory_id}/users` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | add_territory_user |
| GET | `/api/v1/crm/webhooks` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_webhooks |
| POST | `/api/v1/crm/webhooks` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | create_webhook |
| DELETE | `/api/v1/crm/webhooks/{webhook_id}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | delete_webhook |
| PATCH | `/api/v1/crm/webhooks/{webhook_id}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | update_webhook |
| GET | `/api/v1/crm/webhooks/{webhook_id}/deliveries` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_webhook_deliveries |
| POST | `/api/v1/crm/webhooks/{webhook_id}/test` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | test_webhook |
| GET | `/api/v1/crm/{entity}` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | list_records |
| POST | `/api/v1/crm/{entity}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | create_record |
| DELETE | `/api/v1/crm/{entity}/{record_id}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | delete_record |
| GET | `/api/v1/crm/{entity}/{record_id}` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | get_record |
| PATCH | `/api/v1/crm/{entity}/{record_id}` | RequirePermission, get_current_user | crm_admin, crm_manage | - | - | CRM | update_record |
| GET | `/api/v1/crm/{entity}/{record_id}/related` | RequirePermission, get_current_user | crm_admin, crm_manage, crm_view | - | - | CRM | get_related_records |
| GET | `/api/v1/custom-fields/definitions` | RequirePermission, get_current_user | settings_view | - | - | Custom Fields | list_custom_field_definitions |
| POST | `/api/v1/custom-fields/definitions` | RequirePermission, get_current_user | settings_manage | - | - | Custom Fields | create_custom_field_definition |
| GET | `/api/v1/custom-fields/forms` | RequirePermission, get_current_user | settings_view | - | - | Custom Fields | list_custom_forms |
| POST | `/api/v1/custom-fields/forms` | RequirePermission, get_current_user | settings_manage | - | - | Custom Fields | create_custom_form |
| PUT | `/api/v1/custom-fields/forms/submissions/{submission_id}/review` | RequirePermission, get_current_user | settings_manage | - | - | Custom Fields | review_custom_form_submission |
| GET | `/api/v1/custom-fields/forms/{form_id}` | RequirePermission, get_current_user | settings_view | - | - | Custom Fields | get_custom_form |
| GET | `/api/v1/custom-fields/forms/{form_id}/submissions` | RequirePermission, get_current_user | settings_view | - | - | Custom Fields | list_custom_form_submissions |
| POST | `/api/v1/custom-fields/forms/{form_id}/submissions` | RequirePermission, get_current_user | settings_manage | - | - | Custom Fields | submit_custom_form |
| GET | `/api/v1/custom-fields/values` | RequirePermission, get_current_user | settings_view | - | - | Custom Fields | list_custom_field_values |
| PUT | `/api/v1/custom-fields/values` | RequirePermission, get_current_user | settings_manage | - | - | Custom Fields | upsert_custom_field_value |
| GET | `/api/v1/docs` | NONE | - | - | - | - | swagger_ui_html |
| HEAD | `/api/v1/docs` | NONE | - | - | - | - | swagger_ui_html |
| GET | `/api/v1/documents/certificates` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (current_user.employee, user_has_permission) | Documents & Policies | list_certificates |
| POST | `/api/v1/documents/certificates` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (current_user.employee, user_has_permission) | Documents & Policies | upload_certificate |
| POST | `/api/v1/documents/certificates/exports` | RequirePermission, get_current_user | reports_view | - | - | Documents & Policies | create_certificate_export_log |
| GET | `/api/v1/documents/certificates/import-export` | RequirePermission, get_current_user | employee_view | - | - | Documents & Policies | list_certificate_import_export_batches |
| POST | `/api/v1/documents/certificates/imports` | RequirePermission, get_current_user | employee_update | - | - | Documents & Policies | upload_certificate_import |
| PUT | `/api/v1/documents/certificates/{certificate_id}/verify` | RequirePermission, get_current_user | employee_update | - | - | Documents & Policies | verify_certificate |
| GET | `/api/v1/documents/generated` | RequirePermission, get_current_user | employee_view | - | - | Documents & Policies | list_generated |
| POST | `/api/v1/documents/generated` | RequirePermission, get_current_user | employee_update | - | - | Documents & Policies | create_generated |
| GET | `/api/v1/documents/policies` | RequirePermission, get_current_user | company_view | - | - | Documents & Policies | list_policies |
| POST | `/api/v1/documents/policies` | RequirePermission, get_current_user | company_manage | - | - | Documents & Policies | create_policy |
| GET | `/api/v1/documents/policies/{policy_id}/versions` | RequirePermission, get_current_user | company_view | - | - | Documents & Policies | list_policy_versions |
| POST | `/api/v1/documents/policies/{policy_id}/versions` | RequirePermission, get_current_user | company_manage | - | - | Documents & Policies | publish_policy_version |
| GET | `/api/v1/documents/templates` | RequirePermission, get_current_user | company_view | - | - | Documents & Policies | list_templates |
| POST | `/api/v1/documents/templates` | RequirePermission, get_current_user | company_manage | - | - | Documents & Policies | create_template |
| GET | `/api/v1/employees/` | RequirePermission, get_current_user | employee_view | - | - | Employees | list_employees |
| POST | `/api/v1/employees/` | RequirePermission, get_current_user | employee_create | - | - | Employees | create_employee |
| GET | `/api/v1/employees/birthdays` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_can_manage) | Employees | upcoming_birthdays |
| GET | `/api/v1/employees/change-requests` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (current_user.employee, current_user.employee.id) | Employees | list_employee_change_requests |
| POST | `/api/v1/employees/change-requests` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (current_user.employee, current_user.id) | Employees | create_employee_change_request |
| PUT | `/api/v1/employees/change-requests/{request_id}/review` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (current_user.employee, current_user.id) | Employees | review_employee_change_request |
| GET | `/api/v1/employees/count` | RequirePermission, get_current_user | employee_view | - | - | Employees | employee_count |
| GET | `/api/v1/employees/directory` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_rate_limit_directory_search, _to_directory_item) | Employees | employee_directory |
| GET | `/api/v1/employees/directory/export` | get_current_user | - | MEDIUM - user-only (employee PII, documents) | handler-scoped (_to_directory_item, current_user.employee) | Employees | export_employee_directory |
| GET | `/api/v1/employees/directory/filters` | get_current_user | - | - | - | Employees | employee_directory_filters |
| POST | `/api/v1/employees/directory/report-correction` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (current_user.id) | Employees | report_directory_correction |
| GET | `/api/v1/employees/documents/expiring` | RequirePermission, get_current_user | employee_view | - | - | Employees | list_expiring_employee_documents |
| GET | `/api/v1/employees/export` | RequirePermission, get_current_user | employee_export | - | - | Employees | export_employees |
| POST | `/api/v1/employees/import` | RequirePermission, get_current_user | employee_import | - | - | Employees | import_employees |
| GET | `/api/v1/employees/me` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (current_user.employee, current_user.employee.id) | Employees | get_my_employee_profile |
| GET | `/api/v1/employees/me/completeness` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (current_user.employee, current_user.employee.id) | Employees | my_profile_completeness |
| GET | `/api/v1/employees/org-search` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_rate_limit_directory_search) | Employees | org_search_autocomplete |
| GET | `/api/v1/employees/recent-joiners` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_to_directory_item) | Employees | recent_joiners |
| GET | `/api/v1/employees/stats` | RequirePermission, get_current_user | employee_view | - | - | Employees | employee_stats |
| GET | `/api/v1/employees/user-options` | RequirePermission, get_current_user | employee_update | - | - | Employees | list_employee_user_options |
| GET | `/api/v1/employees/work-anniversaries` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_can_manage) | Employees | upcoming_work_anniversaries |
| DELETE | `/api/v1/employees/{employee_id}` | RequirePermission, get_current_user | employee_delete | - | - | Employees | delete_employee |
| GET | `/api/v1/employees/{employee_id}` | RequirePermission, get_current_user | employee_view | - | - | Employees | get_employee |
| PUT | `/api/v1/employees/{employee_id}` | RequirePermission, get_current_user | employee_update | - | - | Employees | update_employee |
| POST | `/api/v1/employees/{employee_id}/documents` | get_current_user | - | MEDIUM - user-only (employee PII, documents) | handler-scoped (current_user.employee, is_self) | Employees | upload_document |
| PUT | `/api/v1/employees/{employee_id}/documents/{document_id}/verify` | RequirePermission, get_current_user | employee_update | - | - | Employees | verify_employee_document |
| POST | `/api/v1/employees/{employee_id}/education` | RequirePermission, get_current_user | employee_update | - | - | Employees | add_education |
| DELETE | `/api/v1/employees/{employee_id}/education/{edu_id}` | RequirePermission, get_current_user | employee_update | - | - | Employees | delete_education |
| POST | `/api/v1/employees/{employee_id}/experience` | RequirePermission, get_current_user | employee_update | - | - | Employees | add_experience |
| GET | `/api/v1/employees/{employee_id}/lifecycle` | RequirePermission, get_current_user | employee_view | - | - | Employees | list_lifecycle_events |
| POST | `/api/v1/employees/{employee_id}/lifecycle` | RequirePermission, get_current_user | employee_update | - | - | Employees | add_lifecycle_event |
| POST | `/api/v1/employees/{employee_id}/photo` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (current_user.employee, is_self) | Employees | upload_photo |
| GET | `/api/v1/employees/{employee_id}/profile-card` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_can_view, _can_view_contact) | Employees | employee_profile_card |
| POST | `/api/v1/employees/{employee_id}/skills` | RequirePermission, get_current_user | employee_update | - | - | Employees | add_skill |
| PUT | `/api/v1/employees/{employee_id}/user-link` | RequirePermission, get_current_user | employee_update | - | - | Employees | update_employee_user_link |
| GET | `/api/v1/engagement/announcements` | get_current_user | - | - | - | Engagement | list_announcements |
| POST | `/api/v1/engagement/announcements` | RequirePermission, get_current_user | notification_manage | - | - | Engagement | create_announcement |
| GET | `/api/v1/engagement/recognition-wall` | get_current_user | - | - | - | Engagement | recognition_wall |
| GET | `/api/v1/engagement/recognitions` | get_current_user | - | - | - | Engagement | list_recognitions |
| POST | `/api/v1/engagement/recognitions` | get_current_user | - | - | - | Engagement | create_recognition |
| POST | `/api/v1/engagement/recognitions/{recognition_id}/reactions` | get_current_user | - | - | - | Engagement | react_to_recognition |
| POST | `/api/v1/engagement/survey-responses` | get_current_user | - | - | - | Engagement | submit_survey_response |
| GET | `/api/v1/engagement/surveys` | get_current_user | - | - | - | Engagement | list_surveys |
| POST | `/api/v1/engagement/surveys` | RequirePermission, get_current_user | performance_manage | - | - | Engagement | create_survey |
| GET | `/api/v1/engagement/surveys/{survey_id}/results` | get_current_user | - | - | - | Engagement | survey_results |
| GET | `/api/v1/enterprise/consents` | RequirePermission, get_current_user | settings_view | - | - | Enterprise Platform | list_consents |
| POST | `/api/v1/enterprise/consents` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | create_consent |
| PUT | `/api/v1/enterprise/consents/{consent_id}/revoke` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | revoke_consent |
| GET | `/api/v1/enterprise/integration-credentials` | RequirePermission, get_current_user | settings_view | - | - | Enterprise Platform | list_integration_credentials |
| POST | `/api/v1/enterprise/integration-credentials` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | create_integration_credential |
| GET | `/api/v1/enterprise/integration-events` | RequirePermission, get_current_user | settings_view | - | - | Enterprise Platform | list_integration_events |
| POST | `/api/v1/enterprise/integration-events` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | queue_integration_event |
| GET | `/api/v1/enterprise/legal-holds` | RequirePermission, get_current_user | settings_view | - | - | Enterprise Platform | list_legal_holds |
| POST | `/api/v1/enterprise/legal-holds` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | create_legal_hold |
| PUT | `/api/v1/enterprise/legal-holds/{hold_id}/release` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | release_legal_hold |
| GET | `/api/v1/enterprise/metrics` | RequirePermission, get_current_user | reports_view | - | - | Enterprise Platform | list_metric_definitions |
| POST | `/api/v1/enterprise/metrics` | RequirePermission, get_current_user | reports_manage | - | - | Enterprise Platform | create_metric_definition |
| GET | `/api/v1/enterprise/privacy-requests` | RequirePermission, get_current_user | settings_view | - | - | Enterprise Platform | list_privacy_requests |
| POST | `/api/v1/enterprise/privacy-requests` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | create_privacy_request |
| PUT | `/api/v1/enterprise/privacy-requests/{request_id}` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | review_privacy_request |
| GET | `/api/v1/enterprise/retention-policies` | RequirePermission, get_current_user | settings_view | - | - | Enterprise Platform | list_retention_policies |
| POST | `/api/v1/enterprise/retention-policies` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | create_retention_policy |
| GET | `/api/v1/enterprise/webhooks` | RequirePermission, get_current_user | settings_view | - | - | Enterprise Platform | list_webhook_subscriptions |
| POST | `/api/v1/enterprise/webhooks` | RequirePermission, get_current_user | settings_manage | - | - | Enterprise Platform | create_webhook_subscription |
| POST | `/api/v1/exit/checklist` | RequirePermission, get_current_user | exit_manage | - | - | Exit Management | create_checklist_item |
| PUT | `/api/v1/exit/checklist/{item_id}/complete` | RequirePermission, get_current_user | exit_manage | - | - | Exit Management | complete_checklist_item |
| GET | `/api/v1/exit/records` | RequirePermission, get_current_user | exit_view | - | - | Exit Management | list_exit_records |
| POST | `/api/v1/exit/records` | RequirePermission, get_current_user | exit_manage | - | - | Exit Management | create_exit_record |
| PUT | `/api/v1/exit/records/{record_id}` | RequirePermission, get_current_user | exit_manage | - | - | Exit Management | update_exit_record |
| PUT | `/api/v1/exit/records/{record_id}/approve` | RequirePermission, get_current_user | exit_manage | - | - | Exit Management | approve_exit_record |
| GET | `/api/v1/helpdesk/analytics` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | helpdesk_analytics |
| GET | `/api/v1/helpdesk/categories` | get_current_user | - | - | - | HR Helpdesk | list_categories |
| POST | `/api/v1/helpdesk/categories` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | create_category |
| GET | `/api/v1/helpdesk/escalation-rules` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | list_escalation_rules |
| POST | `/api/v1/helpdesk/escalation-rules` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | create_escalation_rule |
| GET | `/api/v1/helpdesk/knowledge` | get_current_user | - | - | - | HR Helpdesk | list_knowledge_articles |
| POST | `/api/v1/helpdesk/knowledge` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | create_knowledge_article |
| GET | `/api/v1/helpdesk/sla/breaches` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | list_sla_breaches |
| GET | `/api/v1/helpdesk/tickets` | get_current_user | - | - | - | HR Helpdesk | list_tickets |
| POST | `/api/v1/helpdesk/tickets` | get_current_user | - | - | - | HR Helpdesk | create_ticket |
| GET | `/api/v1/helpdesk/tickets/{ticket_id}` | get_current_user | - | - | - | HR Helpdesk | get_ticket |
| PUT | `/api/v1/helpdesk/tickets/{ticket_id}/assign` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | assign_ticket |
| PUT | `/api/v1/helpdesk/tickets/{ticket_id}/csat` | get_current_user | - | - | - | HR Helpdesk | submit_csat |
| PUT | `/api/v1/helpdesk/tickets/{ticket_id}/escalate` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | escalate_ticket |
| GET | `/api/v1/helpdesk/tickets/{ticket_id}/replies` | get_current_user | - | - | - | HR Helpdesk | get_replies |
| POST | `/api/v1/helpdesk/tickets/{ticket_id}/reply` | get_current_user | - | - | - | HR Helpdesk | add_reply |
| PUT | `/api/v1/helpdesk/tickets/{ticket_id}/status` | RequirePermission, get_current_user | helpdesk_manage | - | - | HR Helpdesk | update_ticket_status |
| POST | `/api/v1/hrms/compliance/esi/generate` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Compliance Exports | generate_esi |
| GET | `/api/v1/hrms/compliance/esi/preview` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Compliance Exports | preview_esi |
| GET | `/api/v1/hrms/compliance/exports/{export_id}/download` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Compliance Exports | download_export |
| POST | `/api/v1/hrms/compliance/pf-ecr/generate` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Compliance Exports | generate_pf_ecr |
| GET | `/api/v1/hrms/compliance/pf-ecr/preview` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Compliance Exports | preview_pf_ecr |
| POST | `/api/v1/hrms/employees/{employee_id}/change-request` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_can_manage, current_user.employee) | HRMS Profile Change Requests | create_profile_change_request |
| GET | `/api/v1/hrms/employees/{employee_id}/tax-declarations` | get_current_user | - | MEDIUM - user-only (payroll, employee PII) | handler-scoped (_can_manage) | HRMS Tax Declaration | get_employee_tax_declarations |
| GET | `/api/v1/hrms/fnf-settlements` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Full & Final Settlement | list_fnf_settlements |
| POST | `/api/v1/hrms/fnf-settlements/generate` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Full & Final Settlement | generate_fnf_settlement |
| GET | `/api/v1/hrms/fnf-settlements/{settlement_id}` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (_enforce_) | HRMS Full & Final Settlement | get_fnf_settlement |
| PATCH | `/api/v1/hrms/fnf-settlements/{settlement_id}` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Full & Final Settlement | update_fnf_settlement |
| POST | `/api/v1/hrms/fnf-settlements/{settlement_id}/approve` | RequirePermission, get_current_user | payroll_approve | - | - | HRMS Full & Final Settlement | approve_fnf_settlement |
| POST | `/api/v1/hrms/fnf-settlements/{settlement_id}/mark-paid` | RequirePermission, get_current_user | payroll_approve, payroll_run | - | - | HRMS Full & Final Settlement | mark_fnf_settlement_paid |
| GET | `/api/v1/hrms/fnf-settlements/{settlement_id}/pdf` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (_enforce_) | HRMS Full & Final Settlement | download_fnf_statement |
| POST | `/api/v1/hrms/fnf-settlements/{settlement_id}/reject` | RequirePermission, get_current_user | payroll_approve | - | - | HRMS Full & Final Settlement | reject_fnf_settlement |
| POST | `/api/v1/hrms/fnf-settlements/{settlement_id}/submit` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Full & Final Settlement | submit_fnf_settlement |
| GET | `/api/v1/hrms/form16` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (_can_manage, current_user.employee) | HRMS Form 16 | list_form16 |
| POST | `/api/v1/hrms/form16/generate` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Form 16 | generate_form16 |
| GET | `/api/v1/hrms/form16/{record_id}/download` | get_current_user | - | MEDIUM - user-only (payroll, documents) | handler-scoped (_enforce_) | HRMS Form 16 | download_form16 |
| POST | `/api/v1/hrms/form16/{record_id}/publish` | RequirePermission, get_current_user | payroll_approve, payroll_run | - | - | HRMS Form 16 | publish_form16 |
| POST | `/api/v1/hrms/form16/{record_id}/upload-part-a` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Form 16 | upload_part_a |
| GET | `/api/v1/hrms/leave-encashment` | get_current_user | - | - | - | HRMS Leave Payroll | list_leave_encashment_requests |
| POST | `/api/v1/hrms/leave-encashment/request` | get_current_user | - | - | - | HRMS Leave Payroll | create_leave_encashment_request |
| POST | `/api/v1/hrms/leave-encashment/{request_id}/approve` | RequirePermission, get_current_user | leave_approve, payroll_run | - | - | HRMS Leave Payroll | approve_leave_encashment_request |
| POST | `/api/v1/hrms/leave-encashment/{request_id}/reject` | RequirePermission, get_current_user | leave_approve, payroll_run | - | - | HRMS Leave Payroll | reject_leave_encashment_request |
| GET | `/api/v1/hrms/payroll/bank-exports/{export_id}/download` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Payroll Bank Advice | download_bank_export |
| GET | `/api/v1/hrms/payroll/lwp-feed` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Leave Payroll | get_lwp_feed |
| POST | `/api/v1/hrms/payroll/lwp-sync` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Leave Payroll | sync_lwp_feed |
| POST | `/api/v1/hrms/payroll/{payroll_run_id}/bank-advice/generate` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Payroll Bank Advice | generate_bank_advice |
| GET | `/api/v1/hrms/payroll/{payroll_run_id}/bank-advice/preview` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Payroll Bank Advice | preview_bank_advice |
| GET | `/api/v1/hrms/payroll/{payroll_run_id}/bank-exports` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Payroll Bank Advice | list_bank_exports |
| POST | `/api/v1/hrms/probation/alerts/run` | RequirePermission, get_current_user | employee_update, employee_view | - | - | HRMS Probation | run_probation_alerts |
| GET | `/api/v1/hrms/probation/dashboard` | get_current_user | - | - | - | HRMS Probation | probation_dashboard |
| GET | `/api/v1/hrms/probation/due-list` | get_current_user | - | - | - | HRMS Probation | probation_due_list |
| POST | `/api/v1/hrms/probation/{employee_id}/confirm` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_perform_action) | HRMS Probation | confirm_probation |
| POST | `/api/v1/hrms/probation/{employee_id}/extend` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_perform_action) | HRMS Probation | extend_probation |
| GET | `/api/v1/hrms/probation/{employee_id}/letter` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_ensure_manager_or_hr) | HRMS Probation | probation_letter |
| POST | `/api/v1/hrms/probation/{employee_id}/review` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_ensure_manager_or_hr, current_user.employee) | HRMS Probation | submit_probation_review |
| POST | `/api/v1/hrms/probation/{employee_id}/terminate` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_perform_action) | HRMS Probation | terminate_probation |
| GET | `/api/v1/hrms/profile-change-requests` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_can_view, _query_accessible_requests) | HRMS Profile Change Requests | list_profile_change_requests |
| GET | `/api/v1/hrms/profile-change-requests/{request_id}` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_query_accessible_requests) | HRMS Profile Change Requests | get_profile_change_request |
| POST | `/api/v1/hrms/profile-change-requests/{request_id}/approve` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_review_request) | HRMS Profile Change Requests | approve_profile_change_request |
| POST | `/api/v1/hrms/profile-change-requests/{request_id}/reject` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (_review_request) | HRMS Profile Change Requests | reject_profile_change_request |
| GET | `/api/v1/hrms/shift-roster` | get_current_user | - | - | - | HRMS Shift Roster | list_shift_roster |
| POST | `/api/v1/hrms/shift-roster/assign` | RequirePermission, get_current_user | attendance_manage | - | - | HRMS Shift Roster | assign_shift_roster |
| POST | `/api/v1/hrms/shift-roster/bulk-assign` | RequirePermission, get_current_user | attendance_manage | - | - | HRMS Shift Roster | bulk_assign_shift_roster |
| POST | `/api/v1/hrms/shift-roster/copy-week` | RequirePermission, get_current_user | attendance_manage | - | - | HRMS Shift Roster | copy_week_shift_roster |
| POST | `/api/v1/hrms/shift-roster/publish` | RequirePermission, get_current_user | attendance_manage | - | - | HRMS Shift Roster | publish_shift_roster |
| DELETE | `/api/v1/hrms/shift-roster/{roster_id}` | RequirePermission, get_current_user | attendance_manage | - | - | HRMS Shift Roster | delete_shift_roster |
| GET | `/api/v1/hrms/tax-declaration/categories` | get_current_user | - | - | - | HRMS Tax Declaration | list_tax_declaration_categories |
| POST | `/api/v1/hrms/tax-declaration/categories` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Tax Declaration | create_tax_declaration_category |
| GET | `/api/v1/hrms/tax-declarations` | RequirePermission, get_current_user | payroll_run, payroll_view | - | - | HRMS Tax Declaration | list_tax_declarations_for_review |
| POST | `/api/v1/hrms/tax-declarations` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (_can_manage, current_user.employee) | HRMS Tax Declaration | create_tax_declaration |
| PATCH | `/api/v1/hrms/tax-declarations/{declaration_id}` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (_enforce_) | HRMS Tax Declaration | update_tax_declaration |
| POST | `/api/v1/hrms/tax-declarations/{declaration_id}/review` | RequirePermission, get_current_user | payroll_run | - | - | HRMS Tax Declaration | review_tax_declaration |
| POST | `/api/v1/hrms/tax-declarations/{declaration_id}/submit` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (_enforce_) | HRMS Tax Declaration | submit_tax_declaration |
| POST | `/api/v1/hrms/tax-declarations/{declaration_id}/upload-proof` | get_current_user | - | MEDIUM - user-only (payroll, documents) | handler-scoped (_enforce_) | HRMS Tax Declaration | upload_tax_proof |
| GET | `/api/v1/hrms/tax-proofs/{proof_id}/download` | get_current_user | - | MEDIUM - user-only (payroll, documents) | handler-scoped (_enforce_) | HRMS Tax Declaration | download_tax_proof |
| POST | `/api/v1/leave/apply` | get_current_user | - | - | - | Leave Management | apply_leave |
| GET | `/api/v1/leave/balance` | get_current_user | - | - | - | Leave Management | my_leave_balance |
| POST | `/api/v1/leave/balance/allocate` | RequirePermission, get_current_user | leave_manage | - | - | Leave Management | allocate_leave |
| GET | `/api/v1/leave/balance/{employee_id}` | RequirePermission, get_current_user | leave_manage | - | - | Leave Management | employee_leave_balance |
| GET | `/api/v1/leave/calendar` | get_current_user | - | - | - | Leave Management | leave_calendar |
| GET | `/api/v1/leave/ledger` | get_current_user | - | - | - | Leave Management | my_leave_ledger |
| GET | `/api/v1/leave/ledger/{employee_id}` | RequirePermission, get_current_user | leave_manage | - | - | Leave Management | employee_leave_ledger |
| GET | `/api/v1/leave/my-requests` | get_current_user | - | - | - | Leave Management | my_leave_requests |
| GET | `/api/v1/leave/pending-count` | RequirePermission, get_current_user | leave_manage | - | - | Leave Management | pending_leave_count |
| GET | `/api/v1/leave/requests` | RequirePermission, get_current_user | leave_approve | - | - | Leave Management | all_leave_requests |
| PUT | `/api/v1/leave/requests/{request_id}/approve` | RequirePermission, get_current_user | leave_approve | - | - | Leave Management | approve_leave |
| PUT | `/api/v1/leave/requests/{request_id}/cancel` | get_current_user | - | - | - | Leave Management | cancel_leave |
| GET | `/api/v1/leave/types` | get_current_user | - | - | - | Leave Management | list_leave_types |
| POST | `/api/v1/leave/types` | RequirePermission, get_current_user | leave_manage | - | - | Leave Management | create_leave_type |
| DELETE | `/api/v1/leave/types/{type_id}` | RequirePermission, get_current_user | leave_manage | - | - | Leave Management | delete_leave_type |
| PUT | `/api/v1/leave/types/{type_id}` | RequirePermission, get_current_user | leave_manage | - | - | Leave Management | update_leave_type |
| GET | `/api/v1/lms/assignments` | get_current_user | - | - | - | Learning | list_assignments |
| POST | `/api/v1/lms/assignments` | RequirePermission, get_current_user | performance_manage | - | - | Learning | assign_course |
| PUT | `/api/v1/lms/assignments/{assignment_id}` | get_current_user | - | - | - | Learning | update_assignment |
| GET | `/api/v1/lms/certifications` | get_current_user | - | - | - | Learning | list_certifications |
| POST | `/api/v1/lms/certifications` | RequirePermission, get_current_user | performance_manage | - | - | Learning | create_certification |
| GET | `/api/v1/lms/courses` | get_current_user | - | - | - | Learning | list_courses |
| POST | `/api/v1/lms/courses` | RequirePermission, get_current_user | performance_manage | - | - | Learning | create_course |
| GET | `/api/v1/logs/analysis` | RequirePermission, get_current_user | company_manage | - | - | Admin Logs | log_analysis |
| GET | `/api/v1/logs/audit` | RequirePermission, get_current_user | company_manage | - | - | Admin Logs | list_audit_logs |
| GET | `/api/v1/logs/errors` | RequirePermission, get_current_user | company_manage | - | - | Admin Logs | list_error_logs |
| GET | `/api/v1/notifications/` | get_current_user | - | - | - | Notifications | list_notifications |
| POST | `/api/v1/notifications/` | RequirePermission, get_current_user | notification_manage | - | - | Notifications | create_manual_notification |
| PUT | `/api/v1/notifications/mark-all-read` | get_current_user | - | - | - | Notifications | mark_all_notifications_read |
| POST | `/api/v1/notifications/people-moments/run` | RequirePermission, get_current_user | notification_manage | - | - | Notifications | run_people_moment_notifications |
| GET | `/api/v1/notifications/unread-count` | get_current_user | - | - | - | Notifications | unread_count |
| PATCH | `/api/v1/notifications/{notification_id}/read` | get_current_user | - | - | - | Notifications | mark_notification_read |
| PUT | `/api/v1/notifications/{notification_id}/read` | get_current_user | - | - | - | Notifications | mark_notification_read |
| GET | `/api/v1/onboarding/employees` | RequirePermission, get_current_user | employee_view | - | - | Onboarding | list_employee_onboarding |
| POST | `/api/v1/onboarding/employees` | RequirePermission, get_current_user | employee_update | - | - | Onboarding | start_employee_onboarding |
| PUT | `/api/v1/onboarding/employees/{onboarding_id}/complete` | RequirePermission, get_current_user | employee_update | - | - | Onboarding | complete_onboarding |
| POST | `/api/v1/onboarding/policy-acknowledgements` | RequirePermission, get_current_user | ai_assistant | - | - | Onboarding | acknowledge_policy |
| GET | `/api/v1/onboarding/templates` | RequirePermission, get_current_user | employee_view | - | - | Onboarding | list_templates |
| POST | `/api/v1/onboarding/templates` | RequirePermission, get_current_user | employee_update | - | - | Onboarding | create_template |
| GET | `/api/v1/openapi.json` | NONE | - | - | - | - | openapi |
| HEAD | `/api/v1/openapi.json` | NONE | - | - | - | - | openapi |
| GET | `/api/v1/payroll/accounting/gl-mappings` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_gl_mappings |
| POST | `/api/v1/payroll/accounting/gl-mappings` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_gl_mapping |
| GET | `/api/v1/payroll/accounting/ledgers` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_accounting_ledgers |
| POST | `/api/v1/payroll/accounting/ledgers` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_accounting_ledger |
| GET | `/api/v1/payroll/arrear-runs` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_payroll_arrear_runs |
| POST | `/api/v1/payroll/arrear-runs` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_payroll_arrear_run |
| GET | `/api/v1/payroll/component-categories` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_component_categories |
| POST | `/api/v1/payroll/component-categories` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_component_category |
| GET | `/api/v1/payroll/component-formula-rules` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_component_formula_rules |
| POST | `/api/v1/payroll/component-formula-rules` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_component_formula_rule |
| GET | `/api/v1/payroll/components` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_components |
| POST | `/api/v1/payroll/components` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_component |
| DELETE | `/api/v1/payroll/components/{component_id}` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | delete_component |
| PUT | `/api/v1/payroll/components/{component_id}` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | update_component |
| GET | `/api/v1/payroll/exports/{batch_id}/download` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | download_payroll_export |
| GET | `/api/v1/payroll/inputs/attendance` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_payroll_attendance_inputs |
| POST | `/api/v1/payroll/inputs/attendance` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | upsert_payroll_attendance_input |
| GET | `/api/v1/payroll/inputs/leave-encashment-lines` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_leave_encashment_lines |
| POST | `/api/v1/payroll/inputs/leave-encashment-lines` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_leave_encashment_line |
| GET | `/api/v1/payroll/inputs/leave-encashment-policies` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_leave_encashment_policies |
| POST | `/api/v1/payroll/inputs/leave-encashment-policies` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_leave_encashment_policy |
| GET | `/api/v1/payroll/inputs/lop-adjustments` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_lop_adjustments |
| POST | `/api/v1/payroll/inputs/lop-adjustments` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_lop_adjustment |
| PUT | `/api/v1/payroll/inputs/lop-adjustments/{adjustment_id}/review` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | review_lop_adjustment |
| GET | `/api/v1/payroll/inputs/overtime-lines` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_overtime_lines |
| POST | `/api/v1/payroll/inputs/overtime-lines` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_overtime_line |
| GET | `/api/v1/payroll/inputs/overtime-policies` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_overtime_policies |
| POST | `/api/v1/payroll/inputs/overtime-policies` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_overtime_policy |
| POST | `/api/v1/payroll/inputs/reconcile-attendance` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | reconcile_payroll_attendance_inputs |
| GET | `/api/v1/payroll/last-run` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | get_last_payroll_run |
| GET | `/api/v1/payroll/loans` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_employee_loans |
| POST | `/api/v1/payroll/loans` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_employee_loan |
| GET | `/api/v1/payroll/loans/{loan_id}/installments` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_loan_installments |
| GET | `/api/v1/payroll/loans/{loan_id}/ledger` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_loan_ledger |
| PUT | `/api/v1/payroll/manual-inputs/{input_id}/review` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | review_manual_input |
| GET | `/api/v1/payroll/off-cycle-runs` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_off_cycle_payroll_runs |
| POST | `/api/v1/payroll/off-cycle-runs` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_off_cycle_payroll_run |
| GET | `/api/v1/payroll/payments/batches` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_payment_batches |
| POST | `/api/v1/payroll/payments/batches` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_payment_batch |
| PUT | `/api/v1/payroll/payments/batches/{batch_id}/status-import` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | import_payment_status |
| GET | `/api/v1/payroll/payslip` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (_can_view, current_user.employee) | Payroll | get_payslip |
| GET | `/api/v1/payroll/payslip/{record_id}/pdf` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (_can_view, current_user.employee) | Payroll | download_payslip_pdf |
| POST | `/api/v1/payroll/payslip/{record_id}/pdf` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | generate_payslip_pdf |
| GET | `/api/v1/payroll/reimbursements` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (current_user.employee, current_user.employee.id) | Payroll | list_reimbursements |
| POST | `/api/v1/payroll/reimbursements` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (current_user.employee, current_user.id) | Payroll | create_reimbursement |
| GET | `/api/v1/payroll/reimbursements/{reimbursement_id}/ledger` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | get_reimbursement_ledger |
| PUT | `/api/v1/payroll/reimbursements/{reimbursement_id}/review` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | review_reimbursement |
| POST | `/api/v1/payroll/run` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | run_payroll |
| GET | `/api/v1/payroll/runs` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_payroll_runs |
| GET | `/api/v1/payroll/runs/{run_id}` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | get_payroll_run |
| POST | `/api/v1/payroll/runs/{run_id}/accounting-journal` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | generate_accounting_journal |
| GET | `/api/v1/payroll/runs/{run_id}/accounting-journals` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_accounting_journals |
| PUT | `/api/v1/payroll/runs/{run_id}/approve` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | approve_payroll |
| GET | `/api/v1/payroll/runs/{run_id}/audit` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | get_payroll_audit |
| GET | `/api/v1/payroll/runs/{run_id}/calculation-snapshots` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_payroll_calculation_snapshots |
| POST | `/api/v1/payroll/runs/{run_id}/exports/{export_type}` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | create_payroll_export |
| GET | `/api/v1/payroll/runs/{run_id}/manual-inputs` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_manual_inputs |
| POST | `/api/v1/payroll/runs/{run_id}/manual-inputs` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_manual_input |
| POST | `/api/v1/payroll/runs/{run_id}/payslip-publish` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | publish_payslips |
| GET | `/api/v1/payroll/runs/{run_id}/pre-run-checks` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_pre_run_checks |
| POST | `/api/v1/payroll/runs/{run_id}/pre-run-checks` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | add_pre_run_check |
| GET | `/api/v1/payroll/runs/{run_id}/records` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | get_payroll_records |
| POST | `/api/v1/payroll/runs/{run_id}/unlock-requests` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_unlock_request |
| GET | `/api/v1/payroll/runs/{run_id}/variance` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | get_payroll_variance |
| GET | `/api/v1/payroll/runs/{run_id}/worksheet` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_payroll_worksheet |
| POST | `/api/v1/payroll/runs/{run_id}/worksheet/process` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | process_payroll_worksheet |
| PUT | `/api/v1/payroll/runs/{run_id}/worksheet/{row_id}` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | update_payroll_worksheet_row |
| POST | `/api/v1/payroll/salary` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | set_employee_salary |
| GET | `/api/v1/payroll/salary-audit` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_sensitive_salary_audit |
| POST | `/api/v1/payroll/salary-component-overrides` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_salary_component_override |
| GET | `/api/v1/payroll/salary-revisions` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_salary_revision_requests |
| POST | `/api/v1/payroll/salary-revisions` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_salary_revision_request |
| PUT | `/api/v1/payroll/salary-revisions/{revision_id}/review` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | review_salary_revision_request |
| POST | `/api/v1/payroll/salary-template-assignments` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | assign_salary_template |
| GET | `/api/v1/payroll/salary-templates` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_salary_templates |
| POST | `/api/v1/payroll/salary-templates` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_salary_template |
| GET | `/api/v1/payroll/salary/{employee_id}` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | get_employee_salary_history |
| GET | `/api/v1/payroll/settlements` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_full_final_settlements |
| POST | `/api/v1/payroll/settlements` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_full_final_settlement |
| PUT | `/api/v1/payroll/settlements/{settlement_id}/approve` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | approve_full_final_settlement |
| GET | `/api/v1/payroll/setup/bank-advice-formats` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_bank_advice_formats |
| POST | `/api/v1/payroll/setup/bank-advice-formats` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_bank_advice_format |
| GET | `/api/v1/payroll/setup/calendars` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_payroll_calendars |
| POST | `/api/v1/payroll/setup/calendars` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_payroll_calendar |
| GET | `/api/v1/payroll/setup/compliance-rules` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_compliance_rules |
| POST | `/api/v1/payroll/setup/compliance-rules` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_compliance_rule |
| GET | `/api/v1/payroll/setup/pay-groups` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_pay_groups |
| POST | `/api/v1/payroll/setup/pay-groups` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_pay_group |
| GET | `/api/v1/payroll/setup/periods` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_payroll_periods |
| POST | `/api/v1/payroll/setup/periods` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_payroll_period |
| POST | `/api/v1/payroll/setup/periods/generate` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | generate_payroll_periods |
| PUT | `/api/v1/payroll/setup/periods/{period_id}/lock` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | lock_payroll_period |
| PUT | `/api/v1/payroll/setup/periods/{period_id}/unlock` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | unlock_payroll_period |
| GET | `/api/v1/payroll/setup/statutory-profiles` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_statutory_profiles |
| POST | `/api/v1/payroll/setup/statutory-profiles` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_statutory_profile |
| POST | `/api/v1/payroll/statutory/calculate` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | calculate_statutory_contributions |
| GET | `/api/v1/payroll/statutory/challans` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_statutory_challans |
| POST | `/api/v1/payroll/statutory/challans` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_statutory_challan |
| POST | `/api/v1/payroll/statutory/challans/generate` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | generate_statutory_challan |
| GET | `/api/v1/payroll/statutory/contribution-lines` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_statutory_contribution_lines |
| GET | `/api/v1/payroll/statutory/employee-profiles` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_employee_statutory_profiles |
| POST | `/api/v1/payroll/statutory/employee-profiles` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | upsert_employee_statutory_profile |
| GET | `/api/v1/payroll/statutory/esi-rules` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_esi_rules |
| POST | `/api/v1/payroll/statutory/esi-rules` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_esi_rule |
| POST | `/api/v1/payroll/statutory/file-validations` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | validate_statutory_file |
| GET | `/api/v1/payroll/statutory/gratuity-rules` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_gratuity_rules |
| POST | `/api/v1/payroll/statutory/gratuity-rules` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_gratuity_rule |
| GET | `/api/v1/payroll/statutory/lwf-slabs` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_lwf_slabs |
| POST | `/api/v1/payroll/statutory/lwf-slabs` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_lwf_slab |
| GET | `/api/v1/payroll/statutory/pf-rules` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_pf_rules |
| POST | `/api/v1/payroll/statutory/pf-rules` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_pf_rule |
| GET | `/api/v1/payroll/statutory/pt-slabs` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_pt_slabs |
| POST | `/api/v1/payroll/statutory/pt-slabs` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_pt_slab |
| GET | `/api/v1/payroll/statutory/return-files` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_statutory_return_files |
| POST | `/api/v1/payroll/statutory/return-files` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_statutory_return_file |
| POST | `/api/v1/payroll/statutory/templates/{template_type}` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | generate_statutory_template |
| GET | `/api/v1/payroll/structures` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_structures |
| POST | `/api/v1/payroll/structures` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_structure |
| POST | `/api/v1/payroll/structures/{structure_id}/clone` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | clone_structure |
| GET | `/api/v1/payroll/structures/{structure_id}/formula-graph` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | salary_structure_formula_graph |
| POST | `/api/v1/payroll/structures/{structure_id}/preview` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | preview_structure |
| GET | `/api/v1/payroll/tax/compare` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | compare_tax_regimes |
| GET | `/api/v1/payroll/tax/cycles` | get_current_user | - | - | - | Payroll | list_tax_cycles |
| POST | `/api/v1/payroll/tax/cycles` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_tax_cycle |
| GET | `/api/v1/payroll/tax/declarations` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (current_user.employee, current_user.employee.id) | Payroll | list_tax_declarations |
| POST | `/api/v1/payroll/tax/declarations` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (current_user.employee, current_user.employee.id) | Payroll | create_tax_declaration |
| PUT | `/api/v1/payroll/tax/declarations/{declaration_id}/review` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | review_tax_declaration |
| POST | `/api/v1/payroll/tax/elections` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (current_user.employee, current_user.id) | Payroll | elect_tax_regime |
| POST | `/api/v1/payroll/tax/previous-employment` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (current_user.employee, current_user.employee.id) | Payroll | create_previous_employment_tax_detail |
| GET | `/api/v1/payroll/tax/projection` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (current_user.employee, current_user.employee.id) | Payroll | tax_projection |
| POST | `/api/v1/payroll/tax/proofs` | get_current_user | - | MEDIUM - user-only (payroll) | handler-scoped (current_user.employee, current_user.employee.id) | Payroll | submit_tax_proof |
| PUT | `/api/v1/payroll/tax/proofs/{proof_id}/verify` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | verify_tax_proof |
| GET | `/api/v1/payroll/tax/regimes` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_tax_regimes |
| POST | `/api/v1/payroll/tax/regimes` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_tax_regime |
| GET | `/api/v1/payroll/tax/section-limits` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_tax_section_limits |
| POST | `/api/v1/payroll/tax/section-limits` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_tax_section_limit |
| GET | `/api/v1/payroll/tax/sections` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_tax_sections |
| POST | `/api/v1/payroll/tax/sections` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_tax_section |
| GET | `/api/v1/payroll/tax/slabs` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | list_tax_slabs |
| POST | `/api/v1/payroll/tax/slabs` | RequirePermission, get_current_user | payroll_run | - | - | Payroll | create_tax_slab |
| POST | `/api/v1/payroll/tax/worksheets/project` | RequirePermission, get_current_user | payroll_view | - | - | Payroll | project_tax_worksheet |
| PUT | `/api/v1/payroll/unlock-requests/{request_id}/review` | RequirePermission, get_current_user | payroll_approve | - | - | Payroll | review_unlock_request |
| GET | `/api/v1/performance/360-feedback-requests` | RequirePermission, get_current_user | performance_view | - | - | Performance Management | list_360_requests |
| POST | `/api/v1/performance/360-feedback-requests` | RequirePermission, get_current_user | performance_manage | - | - | Performance Management | create_360_request |
| PUT | `/api/v1/performance/360-feedback-requests/{request_id}/submit` | get_current_user | - | - | - | Performance Management | submit_360_feedback |
| GET | `/api/v1/performance/360/requests` | RequirePermission, get_current_user | performance_view | - | - | Performance Management | list_360_requests |
| POST | `/api/v1/performance/360/requests` | RequirePermission, get_current_user | performance_manage | - | - | Performance Management | create_360_request |
| PUT | `/api/v1/performance/360/requests/{request_id}/submit` | get_current_user | - | - | - | Performance Management | submit_360_feedback |
| POST | `/api/v1/performance/compensation/cycles` | RequirePermission, get_current_user | payroll_run | - | - | Performance Management | create_compensation_cycle |
| POST | `/api/v1/performance/compensation/merit-recommendations` | RequirePermission, get_current_user | payroll_run | - | - | Performance Management | create_merit_recommendation |
| PUT | `/api/v1/performance/compensation/merit-recommendations/{recommendation_id}` | RequirePermission, get_current_user | payroll_approve | - | - | Performance Management | review_merit_recommendation |
| POST | `/api/v1/performance/compensation/pay-bands` | RequirePermission, get_current_user | payroll_run | - | - | Performance Management | create_pay_band |
| GET | `/api/v1/performance/competencies` | RequirePermission, get_current_user | performance_view | - | - | Performance Management | list_competencies |
| POST | `/api/v1/performance/competencies` | RequirePermission, get_current_user | performance_manage | - | - | Performance Management | create_competency |
| POST | `/api/v1/performance/competency-assessments` | RequirePermission, get_current_user | performance_manage | - | - | Performance Management | create_competency_assessment |
| GET | `/api/v1/performance/cycles` | get_current_user | - | - | - | Performance Management | list_cycles |
| POST | `/api/v1/performance/cycles` | RequirePermission, get_current_user | performance_manage | - | - | Performance Management | create_cycle |
| PUT | `/api/v1/performance/cycles/{cycle_id}/status` | RequirePermission, get_current_user | performance_manage | - | - | Performance Management | update_cycle_status |
| GET | `/api/v1/performance/employees/{employee_id}/skill-gap` | RequirePermission, get_current_user | performance_view | - | - | Performance Management | employee_skill_gap |
| GET | `/api/v1/performance/goals` | get_current_user | - | - | - | Performance Management | list_my_goals |
| POST | `/api/v1/performance/goals` | get_current_user | - | - | - | Performance Management | create_goal |
| POST | `/api/v1/performance/goals/check-ins` | get_current_user | - | - | - | Performance Management | create_goal_check_in |
| PUT | `/api/v1/performance/goals/{goal_id}` | get_current_user | - | - | - | Performance Management | update_goal |
| GET | `/api/v1/performance/goals/{goal_id}/check-ins` | get_current_user | - | - | - | Performance Management | list_goal_check_ins |
| GET | `/api/v1/performance/review-templates` | RequirePermission, get_current_user | performance_view | - | - | Performance Management | list_review_templates |
| POST | `/api/v1/performance/review-templates` | RequirePermission, get_current_user | performance_manage | - | - | Performance Management | create_review_template |
| POST | `/api/v1/performance/reviews` | get_current_user | - | - | - | Performance Management | submit_review |
| GET | `/api/v1/performance/reviews/{employee_id}` | RequirePermission, get_current_user | performance_view | - | - | Performance Management | get_employee_reviews |
| POST | `/api/v1/performance/role-skill-requirements` | RequirePermission, get_current_user | performance_manage | - | - | Performance Management | create_role_skill_requirement |
| DELETE | `/api/v1/project-management/attachments/{file_id}` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (_get_file_for_action) | Project Management | Soft-delete an attachment after validating project access. |
| GET | `/api/v1/project-management/attachments/{file_id}/download` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (_get_file_for_action) | Project Management | Authenticated download route for a PMS attachment. |
| GET | `/api/v1/project-management/backlog` | get_current_user | - | - | - | Project Management | Return project backlog plus active/future/completed sprint task groups. |
| POST | `/api/v1/project-management/backlog/reorder` | get_current_user | - | - | - | Project Management | Reorder tasks in the project backlog. |
| DELETE | `/api/v1/project-management/checklist/{item_id}` | get_current_user | - | - | - | Project Management | Delete a checklist item by id. |
| PATCH | `/api/v1/project-management/checklist/{item_id}` | get_current_user | - | - | - | Project Management | Update a checklist item by id. |
| GET | `/api/v1/project-management/clients` | get_current_user | - | - | - | Project Management | List all clients for the organization. |
| POST | `/api/v1/project-management/clients` | get_current_user | - | - | - | Project Management | Create a new client. |
| DELETE | `/api/v1/project-management/clients/{client_id}` | get_current_user | - | - | - | Project Management | Soft delete a client. |
| GET | `/api/v1/project-management/clients/{client_id}` | get_current_user | - | - | - | Project Management | Get a specific client. |
| PATCH | `/api/v1/project-management/clients/{client_id}` | get_current_user | - | - | - | Project Management | Update a client. |
| DELETE | `/api/v1/project-management/comments/{comment_id}` | get_current_user | - | - | - | Project Management | Delete a comment. |
| PATCH | `/api/v1/project-management/comments/{comment_id}` | get_current_user | - | - | - | Project Management | Update a comment. |
| PATCH | `/api/v1/project-management/components/{component_id}` | get_current_user | - | - | - | Project Management | Update a project component. |
| GET | `/api/v1/project-management/dashboard/{project_id}` | get_current_user | - | - | - | Project Management | Get project dashboard metrics. |
| GET | `/api/v1/project-management/dev-integrations` | get_current_user | - | - | - | Project Management | List repository integrations for accessible PMS projects without exposing secrets. |
| POST | `/api/v1/project-management/dev-integrations` | get_current_user | - | - | - | Project Management | Create or update a GitHub/GitLab repository mapping for a PMS project. |
| POST | `/api/v1/project-management/dev-integrations/webhook/github` | NONE | - | - | - | Project Management | Ingest GitHub push and pull request events and link them to task keys. |
| POST | `/api/v1/project-management/dev-integrations/webhook/gitlab` | NONE | - | - | - | Project Management | Ingest GitLab push and merge request events and link them to task keys. |
| DELETE | `/api/v1/project-management/dev-integrations/{integration_id}` | get_current_user | - | - | - | Project Management | Delete a repository integration mapping. |
| PATCH | `/api/v1/project-management/epics/{epic_id}` | get_current_user | - | - | - | Project Management | Update a project epic. |
| PATCH | `/api/v1/project-management/epics/{epic_id}/schedule` | get_current_user | - | - | - | Project Management | Update epic schedule/status from roadmap planning. |
| GET | `/api/v1/project-management/epics/{epic_id}/tasks` | get_current_user | - | - | - | Project Management | List tasks assigned to an epic. |
| GET | `/api/v1/project-management/files` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (accessible_project) | Project Management | List accessible file metadata. |
| POST | `/api/v1/project-management/files` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (get_project_for_action, get_task_project_for_action) | Project Management | Create file metadata. Actual binary upload can be plugged in later. |
| PATCH | `/api/v1/project-management/files/{file_id}` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (get_project_for_action) | Project Management | Update file metadata. |
| GET | `/api/v1/project-management/gantt` | get_current_user | - | - | - | Project Management | Return scheduled tasks and dependencies for the Gantt/timeline view. |
| POST | `/api/v1/project-management/milestones/{milestone_id}/approve` | get_current_user | - | - | - | Project Management | Approve a milestone from the client portal. |
| POST | `/api/v1/project-management/milestones/{milestone_id}/reject` | get_current_user | - | - | - | Project Management | Reject a milestone with a reason. |
| POST | `/api/v1/project-management/milestones/{milestone_id}/submit-approval` | get_current_user | - | - | - | Project Management | Submit a milestone for client approval. |
| GET | `/api/v1/project-management/module-info` | NONE | - | - | - | Project Management | module_info |
| GET | `/api/v1/project-management/notifications` | get_current_user | - | - | - | Project Management | List current user's PMS notifications. |
| PATCH | `/api/v1/project-management/notifications/{notification_id}/read` | get_current_user | - | - | - | Project Management | Mark a PMS notification and linked mention as read. |
| GET | `/api/v1/project-management/portfolio/health-trend` | get_current_user | - | - | - | Project Management | Return lightweight portfolio trend data from current accessible project state. |
| GET | `/api/v1/project-management/portfolio/projects` | get_current_user | - | - | - | Project Management | Return portfolio project table rows for accessible projects. |
| GET | `/api/v1/project-management/portfolio/summary` | get_current_user | - | - | - | Project Management | Return executive portfolio summary for projects visible to the user. |
| GET | `/api/v1/project-management/projects` | get_current_user | - | - | - | Project Management | List all projects for the organization. |
| POST | `/api/v1/project-management/projects` | get_current_user | - | - | - | Project Management | Create a new project. |
| DELETE | `/api/v1/project-management/projects/{project_id}` | get_current_user | - | - | - | Project Management | Soft delete a project. |
| GET | `/api/v1/project-management/projects/{project_id}` | get_current_user | - | - | - | Project Management | Get a specific project. |
| PATCH | `/api/v1/project-management/projects/{project_id}` | get_current_user | - | - | - | Project Management | Update a project. |
| GET | `/api/v1/project-management/projects/{project_id}/activity` | get_current_user | - | - | - | Project Management | Return recent activity for a project or task. |
| GET | `/api/v1/project-management/projects/{project_id}/board` | get_current_user | - | - | - | Project Management | Get Kanban board with columns and tasks. |
| POST | `/api/v1/project-management/projects/{project_id}/board/reorder` | get_current_user | - | - | - | Project Management | Reorder task within or between columns (Drag & Drop). |
| GET | `/api/v1/project-management/projects/{project_id}/components` | get_current_user | - | - | - | Project Management | List project components. |
| POST | `/api/v1/project-management/projects/{project_id}/components` | get_current_user | - | - | - | Project Management | Create a project component. |
| GET | `/api/v1/project-management/projects/{project_id}/epics` | get_current_user | - | - | - | Project Management | List project epics. |
| POST | `/api/v1/project-management/projects/{project_id}/epics` | get_current_user | - | - | - | Project Management | Create a project epic. |
| GET | `/api/v1/project-management/projects/{project_id}/members` | get_current_user | - | - | - | Project Management | List project members visible to project users. |
| POST | `/api/v1/project-management/projects/{project_id}/members` | get_current_user | - | - | - | Project Management | Add a user to a project with a project role. |
| DELETE | `/api/v1/project-management/projects/{project_id}/members/{member_id}` | get_current_user | - | - | - | Project Management | Remove a user from a project. |
| PATCH | `/api/v1/project-management/projects/{project_id}/members/{member_id}` | get_current_user | - | - | - | Project Management | Update a project member role. |
| GET | `/api/v1/project-management/projects/{project_id}/milestones` | get_current_user | - | - | - | Project Management | List all milestones for a project. |
| POST | `/api/v1/project-management/projects/{project_id}/milestones` | get_current_user | - | - | - | Project Management | Create a milestone for a project. |
| GET | `/api/v1/project-management/projects/{project_id}/releases` | get_current_user | - | - | - | Project Management | List project releases. |
| POST | `/api/v1/project-management/projects/{project_id}/releases` | get_current_user | - | - | - | Project Management | Create a project release. |
| GET | `/api/v1/project-management/projects/{project_id}/saved-filters` | get_current_user | - | - | - | Project Management | List user-owned and shared saved filters for a project. |
| POST | `/api/v1/project-management/projects/{project_id}/saved-filters` | get_current_user | - | - | - | Project Management | Save a project board/backlog/report filter. |
| GET | `/api/v1/project-management/projects/{project_id}/sprints` | get_current_user | - | - | - | Project Management | List project sprints. |
| POST | `/api/v1/project-management/projects/{project_id}/sprints` | get_current_user | - | - | - | Project Management | Create a sprint for a project. |
| GET | `/api/v1/project-management/projects/{project_id}/tasks` | get_current_user | - | - | - | Project Management | List all tasks in a project. |
| POST | `/api/v1/project-management/projects/{project_id}/tasks` | get_current_user | - | - | - | Project Management | Create a new task in a project. |
| GET | `/api/v1/project-management/projects/{project_id}/velocity` | get_current_user | - | - | - | Project Management | Return completed sprint velocity history for a project. |
| GET | `/api/v1/project-management/projects/{project_id}/workload` | get_current_user | - | - | - | Project Management | Return capacity/workload grouped by user or sprint. |
| PATCH | `/api/v1/project-management/releases/{release_id}` | get_current_user | - | - | - | Project Management | Update a project release. |
| GET | `/api/v1/project-management/releases/{release_id}/readiness` | get_current_user | - | - | - | Project Management | Summarize release readiness, blockers, severity, and overdue risk. |
| GET | `/api/v1/project-management/reports/burndown` | get_current_user | - | - | - | Project Management | report_burndown |
| GET | `/api/v1/project-management/reports/cumulative-flow` | get_current_user | - | - | - | Project Management | report_cumulative_flow |
| GET | `/api/v1/project-management/reports/cycle-time` | get_current_user | - | - | - | Project Management | report_cycle_time |
| GET | `/api/v1/project-management/reports/export` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (report_task_distribution, report_cycle_time) | Project Management | export_reports |
| GET | `/api/v1/project-management/reports/project-health` | get_current_user | - | - | - | Project Management | report_project_health |
| GET | `/api/v1/project-management/reports/task-distribution` | get_current_user | - | - | - | Project Management | report_task_distribution |
| GET | `/api/v1/project-management/reports/team-performance` | get_current_user | - | - | - | Project Management | report_team_performance |
| GET | `/api/v1/project-management/reports/time-in-status` | get_current_user | - | - | - | Project Management | report_time_in_status |
| GET | `/api/v1/project-management/reports/velocity` | get_current_user | - | - | - | Project Management | report_velocity |
| GET | `/api/v1/project-management/risks` | get_current_user | - | - | - | Project Management | List project risks visible to the current user. |
| POST | `/api/v1/project-management/risks` | get_current_user | - | - | - | Project Management | Create a risk in a project risk register. |
| DELETE | `/api/v1/project-management/risks/{risk_id}` | get_current_user | - | - | - | Project Management | Soft-delete a project risk. |
| PATCH | `/api/v1/project-management/risks/{risk_id}` | get_current_user | - | - | - | Project Management | Update a project risk. |
| GET | `/api/v1/project-management/roadmap` | get_current_user | - | - | - | Project Management | Return cross-project epic roadmap data for accessible projects. |
| DELETE | `/api/v1/project-management/saved-filters/{filter_id}` | get_current_user | - | - | - | Project Management | Delete a saved filter. |
| PATCH | `/api/v1/project-management/saved-filters/{filter_id}` | get_current_user | - | - | - | Project Management | Update a saved filter. |
| GET | `/api/v1/project-management/saved-views` | get_current_user | - | - | - | Project Management | List saved views for the current user and shared workspace/team views. |
| POST | `/api/v1/project-management/saved-views` | get_current_user | - | - | - | Project Management | Create a saved task view with filters, sort state, and visible columns. |
| DELETE | `/api/v1/project-management/saved-views/{view_id}` | get_current_user | - | - | - | Project Management | Delete a saved task view. |
| PATCH | `/api/v1/project-management/saved-views/{view_id}` | get_current_user | - | - | - | Project Management | Update a saved task view. |
| GET | `/api/v1/project-management/sprints/{sprint_id}/burndown` | get_current_user | - | - | - | Project Management | Return a sprint burndown series from commitment and completion dates. |
| POST | `/api/v1/project-management/sprints/{sprint_id}/complete` | get_current_user | - | - | - | Project Management | Complete a sprint and optionally carry unfinished work forward. |
| POST | `/api/v1/project-management/sprints/{sprint_id}/reorder-tasks` | get_current_user | - | - | - | Project Management | Reorder tasks inside one sprint. |
| GET | `/api/v1/project-management/sprints/{sprint_id}/review` | get_current_user | - | - | - | Project Management | Return sprint review notes, retro action items, and completion task split. |
| PATCH | `/api/v1/project-management/sprints/{sprint_id}/review` | get_current_user | - | - | - | Project Management | Update sprint review and retrospective notes without changing sprint status. |
| POST | `/api/v1/project-management/sprints/{sprint_id}/start` | get_current_user | - | - | - | Project Management | Start a sprint and capture the committed scope snapshot. |
| GET | `/api/v1/project-management/tags` | get_current_user | - | - | - | Project Management | List organization-scoped task tags. |
| POST | `/api/v1/project-management/tags` | get_current_user | - | - | - | Project Management | Create an organization-scoped task tag. |
| POST | `/api/v1/project-management/task-dependencies` | get_current_user | - | - | - | Project Management | Create a dependency using Gantt source/target terminology. |
| DELETE | `/api/v1/project-management/task-dependencies/{dependency_id}` | get_current_user | - | - | - | Project Management | Delete a dependency by id. |
| GET | `/api/v1/project-management/tasks` | get_current_user | - | - | - | Project Management | List all accessible PMS tasks for the issue navigator/table view. |
| PATCH | `/api/v1/project-management/tasks/bulk` | get_current_user | - | - | - | Project Management | Bulk update common planning fields across selected tasks. |
| DELETE | `/api/v1/project-management/tasks/{task_id}` | get_current_user | - | - | - | Project Management | Soft delete a task. |
| GET | `/api/v1/project-management/tasks/{task_id}` | get_current_user | - | - | - | Project Management | Get a specific task. |
| PATCH | `/api/v1/project-management/tasks/{task_id}` | get_current_user | - | - | - | Project Management | Update a task. |
| GET | `/api/v1/project-management/tasks/{task_id}/activity` | get_current_user | - | - | - | Project Management | List activity for one task. |
| GET | `/api/v1/project-management/tasks/{task_id}/attachments` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (get_task_project_for_action) | Project Management | List file metadata attached to one task. |
| POST | `/api/v1/project-management/tasks/{task_id}/attachments` | get_current_user | - | MEDIUM - user-only (documents) | handler-scoped (get_task_project_for_action, current_user.id) | Project Management | Upload a binary file and attach it to a task. |
| GET | `/api/v1/project-management/tasks/{task_id}/checklist` | get_current_user | - | - | - | Project Management | Singular checklist alias for task detail consumers. |
| POST | `/api/v1/project-management/tasks/{task_id}/checklist` | get_current_user | - | - | - | Project Management | Singular checklist alias for creating task checklist items. |
| POST | `/api/v1/project-management/tasks/{task_id}/checklist/reorder` | get_current_user | - | - | - | Project Management | Reorder checklist items for one task. |
| GET | `/api/v1/project-management/tasks/{task_id}/checklists` | get_current_user | - | - | - | Project Management | List checklist items for one task. |
| POST | `/api/v1/project-management/tasks/{task_id}/checklists` | get_current_user | - | - | - | Project Management | Create a checklist item for one task. |
| PATCH | `/api/v1/project-management/tasks/{task_id}/checklists/{item_id}` | get_current_user | - | - | - | Project Management | Update a checklist item for one task. |
| GET | `/api/v1/project-management/tasks/{task_id}/comments` | get_current_user | - | - | - | Project Management | List all comments on a task. |
| POST | `/api/v1/project-management/tasks/{task_id}/comments` | get_current_user | - | - | - | Project Management | Add a comment to a task (Collaboration). |
| GET | `/api/v1/project-management/tasks/{task_id}/dependencies` | get_current_user | - | - | - | Project Management | List blockers and dependent work for a task. |
| POST | `/api/v1/project-management/tasks/{task_id}/dependencies` | get_current_user | - | - | - | Project Management | Mark another task as a blocker/dependency for this task. |
| DELETE | `/api/v1/project-management/tasks/{task_id}/dependencies/{dependency_id}` | get_current_user | - | - | - | Project Management | Remove a blocker/dependency link. |
| GET | `/api/v1/project-management/tasks/{task_id}/dev-links` | get_current_user | - | - | - | Project Management | List branches, commits, pull requests, and merge requests linked to a task. |
| GET | `/api/v1/project-management/tasks/{task_id}/links` | get_current_user | - | - | - | Project Management | Alias dependency links for task detail tabs. |
| POST | `/api/v1/project-management/tasks/{task_id}/move-to-sprint` | get_current_user | - | - | - | Project Management | Assign a task to an active or future sprint. |
| POST | `/api/v1/project-management/tasks/{task_id}/remove-from-sprint` | get_current_user | - | - | - | Project Management | Move a task back to the project backlog. |
| PATCH | `/api/v1/project-management/tasks/{task_id}/schedule` | get_current_user | - | - | - | Project Management | Update task start/end dates from the Gantt view. |
| GET | `/api/v1/project-management/tasks/{task_id}/subtasks` | get_current_user | - | - | - | Project Management | List direct sub-tasks for one task. |
| POST | `/api/v1/project-management/tasks/{task_id}/subtasks` | get_current_user | - | - | - | Project Management | Create a child sub-task under an existing task. |
| GET | `/api/v1/project-management/tasks/{task_id}/tags` | get_current_user | - | - | - | Project Management | List tags attached to one task. |
| POST | `/api/v1/project-management/tasks/{task_id}/tags` | get_current_user | - | - | - | Project Management | Attach an organization-scoped tag to one task. |
| DELETE | `/api/v1/project-management/tasks/{task_id}/tags/{tag_id}` | get_current_user | - | - | - | Project Management | Remove a tag from one task without deleting the organization tag. |
| GET | `/api/v1/project-management/tasks/{task_id}/time-logs` | get_current_user | - | - | - | Project Management | List time logs for one task. |
| POST | `/api/v1/project-management/tasks/{task_id}/time-logs` | get_current_user | - | - | - | Project Management | Create a time log entry for one task. |
| GET | `/api/v1/project-management/time-logs` | get_current_user | - | - | - | Project Management | List time logs. |
| POST | `/api/v1/project-management/time-logs` | get_current_user | - | - | - | Project Management | Create a time log entry. |
| DELETE | `/api/v1/project-management/time-logs/{time_log_id}` | get_current_user | - | - | - | Project Management | Delete a time log entry. |
| PATCH | `/api/v1/project-management/time-logs/{time_log_id}` | get_current_user | - | - | - | Project Management | Update a time log entry. |
| GET | `/api/v1/project-management/timesheets` | get_current_user | - | - | - | Project Management | List weekly PMS timesheets scoped to the current user or approver visibility. |
| POST | `/api/v1/project-management/timesheets` | get_current_user | - | - | - | Project Management | Create or return a weekly PMS timesheet for a user. |
| PATCH | `/api/v1/project-management/timesheets/{timesheet_id}` | get_current_user | - | - | - | Project Management | Replace editable weekly timesheet entries. |
| POST | `/api/v1/project-management/timesheets/{timesheet_id}/approve` | get_current_user | - | - | - | Project Management | Approve a submitted PMS timesheet. |
| POST | `/api/v1/project-management/timesheets/{timesheet_id}/reject` | get_current_user | - | - | - | Project Management | Reject a submitted PMS timesheet with comments. |
| POST | `/api/v1/project-management/timesheets/{timesheet_id}/submit` | get_current_user | - | - | - | Project Management | Submit a draft or rejected PMS timesheet for approval. |
| GET | `/api/v1/project-management/users/search` | get_current_user | - | - | - | Project Management | Search mentionable users scoped to a PMS project/task. |
| GET | `/api/v1/project-management/workload` | get_current_user | - | - | - | Project Management | Return assignee-by-week workload and capacity for accessible PMS projects. |
| GET | `/api/v1/recruitment/candidates` | RequirePermission, get_current_user | recruitment_view | - | - | Recruitment ATS | list_candidates |
| POST | `/api/v1/recruitment/candidates` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | create_candidate |
| GET | `/api/v1/recruitment/candidates/{candidate_id}` | RequirePermission, get_current_user | recruitment_view | - | - | Recruitment ATS | get_candidate |
| POST | `/api/v1/recruitment/candidates/{candidate_id}/convert` | RequirePermission, get_current_user | employee_create | - | - | Recruitment ATS | convert_candidate_to_employee |
| GET | `/api/v1/recruitment/candidates/{candidate_id}/interviews` | RequirePermission, get_current_user | recruitment_view | - | - | Recruitment ATS | get_interviews |
| POST | `/api/v1/recruitment/candidates/{candidate_id}/resume` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | upload_resume |
| PUT | `/api/v1/recruitment/candidates/{candidate_id}/status` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | update_candidate_status |
| POST | `/api/v1/recruitment/interviews` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | schedule_interview |
| POST | `/api/v1/recruitment/interviews/{interview_id}/feedback` | get_current_user | - | - | - | Recruitment ATS | add_feedback |
| PUT | `/api/v1/recruitment/interviews/{interview_id}/result` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | update_interview_result |
| GET | `/api/v1/recruitment/jobs` | RequirePermission, get_current_user | recruitment_view | - | - | Recruitment ATS | list_jobs |
| POST | `/api/v1/recruitment/jobs` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | create_job |
| GET | `/api/v1/recruitment/jobs/{job_id}` | RequirePermission, get_current_user | recruitment_view | - | - | Recruitment ATS | get_job |
| PUT | `/api/v1/recruitment/jobs/{job_id}` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | update_job |
| POST | `/api/v1/recruitment/offers` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | create_offer |
| PUT | `/api/v1/recruitment/offers/{offer_id}/status` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | update_offer_status |
| GET | `/api/v1/recruitment/requisitions` | RequirePermission, get_current_user | recruitment_view | - | - | Recruitment ATS | list_requisitions |
| POST | `/api/v1/recruitment/requisitions` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | create_requisition |
| PUT | `/api/v1/recruitment/requisitions/{requisition_id}/review` | RequirePermission, get_current_user | recruitment_manage | - | - | Recruitment ATS | review_requisition |
| GET | `/api/v1/redoc` | NONE | - | - | - | - | redoc_html |
| HEAD | `/api/v1/redoc` | NONE | - | - | - | - | redoc_html |
| GET | `/api/v1/reports/attendance-trend` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | attendance_trend |
| GET | `/api/v1/reports/dashboard` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | dashboard_stats |
| GET | `/api/v1/reports/definitions` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | list_report_definitions |
| POST | `/api/v1/reports/definitions` | RequirePermission, get_current_user | reports_manage | - | - | Reports & Analytics | create_report_definition |
| POST | `/api/v1/reports/definitions/{definition_id}/run` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | run_report_definition |
| GET | `/api/v1/reports/dei-analytics` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | dei_analytics |
| GET | `/api/v1/reports/employee-turnover` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | turnover_report |
| GET | `/api/v1/reports/ess-summary` | get_current_user | - | MEDIUM - user-only (employee PII) | handler-scoped (current_user.employee) | Reports & Analytics | ess_summary |
| GET | `/api/v1/reports/field-catalog` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | report_field_catalog |
| GET | `/api/v1/reports/global-search` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | global_search |
| GET | `/api/v1/reports/headcount-by-department` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | headcount_by_department |
| GET | `/api/v1/reports/leave-trend` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | leave_trend |
| GET | `/api/v1/reports/manager-dashboard` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | manager_dashboard |
| GET | `/api/v1/reports/payroll-summary` | RequirePermission, get_current_user | payroll_view | - | - | Reports & Analytics | payroll_summary |
| GET | `/api/v1/reports/people-moments` | get_current_user | - | - | - | Reports & Analytics | people_moments |
| GET | `/api/v1/reports/project-utilization` | RequirePermission, get_current_user | reports_view | - | - | Reports & Analytics | project_utilization_report |
| GET | `/api/v1/reports/recruitment-funnel` | RequirePermission, get_current_user | recruitment_view | - | - | Reports & Analytics | recruitment_funnel |
| GET | `/api/v1/statutory-compliance/calendar` | RequirePermission, get_current_user | payroll_view | - | - | Statutory Compliance | list_calendar_events |
| POST | `/api/v1/statutory-compliance/calendar` | RequirePermission, get_current_user | payroll_run | - | - | Statutory Compliance | create_calendar_event |
| PUT | `/api/v1/statutory-compliance/calendar/{event_id}` | RequirePermission, get_current_user | payroll_run | - | - | Statutory Compliance | update_calendar_event |
| GET | `/api/v1/statutory-compliance/form16` | RequirePermission, get_current_user | payroll_view | - | - | Statutory Compliance | list_form16 |
| POST | `/api/v1/statutory-compliance/form16` | RequirePermission, get_current_user | payroll_run | - | - | Statutory Compliance | generate_form16 |
| PUT | `/api/v1/statutory-compliance/form16/{document_id}/publish` | RequirePermission, get_current_user | payroll_approve | - | - | Statutory Compliance | publish_form16 |
| GET | `/api/v1/statutory-compliance/legal-entities` | RequirePermission, get_current_user | payroll_view | - | - | Statutory Compliance | list_legal_entities |
| POST | `/api/v1/statutory-compliance/legal-entities` | RequirePermission, get_current_user | payroll_run | - | - | Statutory Compliance | create_legal_entity |
| POST | `/api/v1/statutory-compliance/portal-submissions` | RequirePermission, get_current_user | payroll_run | - | - | Statutory Compliance | create_portal_submission |
| PUT | `/api/v1/statutory-compliance/portal-submissions/{submission_id}/submit` | RequirePermission, get_current_user | payroll_approve | - | - | Statutory Compliance | submit_portal_submission |
| POST | `/api/v1/statutory-compliance/tds-filings` | RequirePermission, get_current_user | payroll_run | - | - | Statutory Compliance | create_tds_filing |
| PUT | `/api/v1/statutory-compliance/tds-filings/{filing_id}/submit` | RequirePermission, get_current_user | payroll_approve | - | - | Statutory Compliance | submit_tds_filing |
| GET | `/api/v1/statutory/calendar` | RequirePermission, get_current_user | payroll_view | - | - | Statutory | list_calendar |
| PUT | `/api/v1/statutory/calendar/{calendar_id}/mark-filed` | RequirePermission, get_current_user | payroll_approve | - | - | Statutory | mark_calendar_filed |
| GET | `/api/v1/statutory/compliance-summary` | RequirePermission, get_current_user | payroll_view | - | - | Statutory | compliance_summary |
| POST | `/api/v1/statutory/generate/{payroll_run_id}/{statutory_type}` | RequirePermission, get_current_user | payroll_run | - | - | Statutory | generate_statutory_file |
| GET | `/api/v1/statutory/submissions` | RequirePermission, get_current_user | payroll_view | - | - | Statutory | list_submissions |
| GET | `/api/v1/statutory/submissions/{submission_id}/download` | RequirePermission, get_current_user | payroll_view | - | - | Statutory | download_submission |
| PUT | `/api/v1/statutory/submissions/{submission_id}/mark-submitted` | RequirePermission, get_current_user | payroll_approve | - | - | Statutory | mark_submission_submitted |
| GET | `/api/v1/timesheets/` | RequirePermission, get_current_user | timesheet_view | - | - | Timesheets | list_timesheets |
| POST | `/api/v1/timesheets/` | RequirePermission, get_current_user | timesheet_view | - | - | Timesheets | create_timesheet |
| GET | `/api/v1/timesheets/projects` | RequirePermission, get_current_user | timesheet_view | - | - | Timesheets | list_projects |
| POST | `/api/v1/timesheets/projects` | RequirePermission, get_current_user | timesheet_manage | - | - | Timesheets | create_project |
| POST | `/api/v1/timesheets/{timesheet_id}/entries` | RequirePermission, get_current_user | timesheet_view | - | - | Timesheets | add_timesheet_entry |
| PUT | `/api/v1/timesheets/{timesheet_id}/review` | RequirePermission, get_current_user | timesheet_approve | - | - | Timesheets | review_timesheet |
| PUT | `/api/v1/timesheets/{timesheet_id}/submit` | RequirePermission, get_current_user | timesheet_view | - | - | Timesheets | submit_timesheet |
| GET | `/api/v1/uploads/{file_path:path}` | get_current_user_for_asset | - | MEDIUM - user-only (documents) | handler-scoped (_safe_upload_path) | Uploads | download_upload |
| GET | `/api/v1/users/search` | get_current_user | - | - | - | Users | search_users |
| GET | `/api/v1/whatsapp-ess/configs` | RequirePermission, get_current_user | notification_manage | - | - | WhatsApp ESS | list_configs |
| POST | `/api/v1/whatsapp-ess/configs` | RequirePermission, get_current_user | notification_manage | - | - | WhatsApp ESS | create_config |
| POST | `/api/v1/whatsapp-ess/delivery-callbacks` | RequirePermission, get_current_user | notification_manage | - | - | WhatsApp ESS | receive_delivery_callback |
| GET | `/api/v1/whatsapp-ess/messages` | RequirePermission, get_current_user | notification_view | - | - | WhatsApp ESS | list_messages |
| POST | `/api/v1/whatsapp-ess/messages/inbound` | RequirePermission, get_current_user | notification_manage | - | - | WhatsApp ESS | receive_inbound_message |
| POST | `/api/v1/whatsapp-ess/messages/outbound` | RequirePermission, get_current_user | notification_manage | - | - | WhatsApp ESS | send_outbound_message |
| POST | `/api/v1/whatsapp-ess/opt-ins` | RequirePermission, get_current_user | notification_manage | - | - | WhatsApp ESS | upsert_opt_in |
| GET | `/api/v1/whatsapp-ess/templates` | RequirePermission, get_current_user | notification_view | - | - | WhatsApp ESS | list_templates |
| POST | `/api/v1/whatsapp-ess/templates` | RequirePermission, get_current_user | notification_manage | - | - | WhatsApp ESS | create_template |
| GET | `/api/v1/workflow-engine/definitions` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | list_definitions |
| POST | `/api/v1/workflow-engine/definitions` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | create_definition |
| DELETE | `/api/v1/workflow-engine/definitions/{definition_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | delete_definition |
| GET | `/api/v1/workflow-engine/definitions/{definition_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | get_definition |
| PUT | `/api/v1/workflow-engine/definitions/{definition_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | update_definition |
| GET | `/api/v1/workflow-engine/definitions/{definition_id}/steps` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | list_definition_steps |
| POST | `/api/v1/workflow-engine/definitions/{definition_id}/steps` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | create_definition_step |
| PUT | `/api/v1/workflow-engine/definitions/{definition_id}/steps/reorder` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | reorder_definition_steps |
| DELETE | `/api/v1/workflow-engine/definitions/{definition_id}/steps/{step_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | delete_definition_step |
| PUT | `/api/v1/workflow-engine/definitions/{definition_id}/steps/{step_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | update_definition_step |
| PUT | `/api/v1/workflow-engine/definitions/{definition_id}/toggle-active` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | toggle_definition |
| POST | `/api/v1/workflow-engine/instances` | get_current_user | - | - | - | Workflow Engine | start_instance |
| GET | `/api/v1/workflow-engine/tasks` | get_current_user | - | - | - | Workflow Engine | my_tasks |
| POST | `/api/v1/workflow-engine/tasks/process-escalations` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | process_escalations |
| POST | `/api/v1/workflow-engine/tasks/send-reminders` | RequirePermission, get_current_user | company_manage | - | - | Workflow Engine | mark_due_reminders |
| PUT | `/api/v1/workflow-engine/tasks/{task_id}/decision` | get_current_user | - | - | - | Workflow Engine | decide_task |
| GET | `/api/v1/workflow/definitions` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | list_workflow_definitions |
| POST | `/api/v1/workflow/definitions` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | create_workflow_definition |
| DELETE | `/api/v1/workflow/definitions/{definition_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | delete_workflow_definition |
| GET | `/api/v1/workflow/definitions/{definition_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | get_workflow_definition |
| PUT | `/api/v1/workflow/definitions/{definition_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | update_workflow_definition |
| POST | `/api/v1/workflow/definitions/{definition_id}/activate` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | activate_workflow_definition |
| POST | `/api/v1/workflow/definitions/{definition_id}/deactivate` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | deactivate_workflow_definition |
| GET | `/api/v1/workflow/definitions/{definition_id}/steps` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | list_workflow_steps |
| POST | `/api/v1/workflow/definitions/{definition_id}/steps` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | add_workflow_step |
| DELETE | `/api/v1/workflow/definitions/{definition_id}/steps/{step_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | delete_workflow_step |
| PUT | `/api/v1/workflow/definitions/{definition_id}/steps/{step_id}` | RequirePermission, get_current_user | company_manage | - | - | Workflow Inbox | update_workflow_step |
| GET | `/api/v1/workflow/inbox` | get_current_user | - | - | - | Workflow Inbox | workflow_inbox |
| GET | `/docs/oauth2-redirect` | public | - | - | - | - | swagger_ui_redirect |
| HEAD | `/docs/oauth2-redirect` | public | - | - | - | - | swagger_ui_redirect |
| GET | `/health` | public | - | - | - | - | health_check |
