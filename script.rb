najiz_data = [
  {contract: '20026496614', version: 1, nin: '1012863278'},
  {contract: '10587474305', version: 1, nin: '1008913442'},
  {contract: '10184529698', version: 1, nin: '1073526616'},
  {contract: '20540057673', version: 1, nin: '1034990638'},
]

application = Domain::Contract::Applications::OutboundApplication.new(auth_context: Ejar3::Iam::AuthenticationService.system_user)
najiz_data.each do |obj|
  pp "Getting Data for #{obj[:contract]}"
  pp application.contract_details_v2(contract_number: obj[:contract], id_number: obj[:nin], major_version: obj[:version])
end
